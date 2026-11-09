from decimal import Decimal
import os
from rest_framework import serializers
from .models import MiNetGrowthLevel


class MiNetGrowthLevelSerializer(serializers.ModelSerializer):
    # Optional read-only helpers for UI convenience
    formatted_lower_range = serializers.SerializerMethodField(read_only=True)
    formatted_upper_range = serializers.SerializerMethodField(read_only=True)
    attachment_name = serializers.SerializerMethodField(read_only=True)
    attachment_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MiNetGrowthLevel
        fields = [
            'id',
            'net_id',
            'level',
            'lower_range',
            'upper_range',
            'percentage',
            'created_date',
            'created_user',
            'updated_date',
            'updated_user',
            'status',
            'attachment',
            'attachment_name',
            'attachment_url',
            'comments',
            'formatted_lower_range',
            'formatted_upper_range',
        ]
        read_only_fields = ['id', 'net_id', 'created_date', 'updated_date']

    def get_formatted_lower_range(self, obj):
        return f"{obj.lower_range:,.2f}" if obj.lower_range is not None else "0.00"

    def get_formatted_upper_range(self, obj):
        return f"{obj.upper_range:,.2f}" if obj.upper_range is not None else "0.00"

    def get_attachment_name(self, obj):
        if obj.attachment:
            return os.path.basename(obj.attachment.name)
        return None

    def get_attachment_url(self, obj):
        request = self.context.get('request')
        if obj.attachment:
            if request is not None:
                return request.build_absolute_uri(obj.attachment.url)
            return obj.attachment.url
        return None

    def to_internal_value(self, data):
        """
        Normalize uppercase keys to lowercase so payloads using
        LEVEL, LOWER_RANGE, UPPER_RANGE, PERCENTAGE, etc. work interchangeably.
        """
        normalized_data = data.copy() if hasattr(data, 'copy') else dict(data)
        key_mappings = {
            'ID': 'id',
            'NET_ID': 'net_id',
            'LEVEL': 'level',
            'LOWER_RANGE': 'lower_range',
            'UPPER_RANGE': 'upper_range',
            'PERCENTAGE': 'percentage',
            'STATUS': 'status',
            'ATTACHMENT': 'attachment',
            'COMMENTS': 'comments',
            'CREATED_USER': 'created_user',
            'UPDATED_USER': 'updated_user',
        }
        for upper_key, lower_key in key_mappings.items():
            if upper_key in normalized_data and lower_key not in normalized_data:
                normalized_data[lower_key] = normalized_data[upper_key]

        return super().to_internal_value(normalized_data)

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)

        lower_range = attrs.get('lower_range', getattr(instance, 'lower_range', None))
        upper_range = attrs.get('upper_range', getattr(instance, 'upper_range', None))
        percentage = attrs.get('percentage', getattr(instance, 'percentage', None))
        status = attrs.get('status', getattr(instance, 'status', 'Active'))

        errors = {}

        # 1. Lower Range non-negative check
        if lower_range is not None and lower_range < Decimal('0'):
            errors['lower_range'] = ['LOWER_RANGE must be greater than or equal to 0.']

        # 2. Upper Range > Lower Range check
        if lower_range is not None and upper_range is not None:
            if upper_range <= lower_range:
                errors['upper_range'] = [
                    f'UPPER_RANGE ({upper_range}) must be strictly greater than LOWER_RANGE ({lower_range}).'
                ]

        # 3. Percentage limit check (0 - 100)
        if percentage is not None:
            if percentage < Decimal('0') or percentage > Decimal('100'):
                errors['percentage'] = ['PERCENTAGE must be between 0.00% and 100.00%.']

        # 4. Overlap check for Active records
        if status == 'Active' and lower_range is not None and upper_range is not None:
            qs = MiNetGrowthLevel.objects.filter(status='Active')
            if instance:
                qs = qs.exclude(pk=instance.pk)

            # Two closed intervals [A, B] and [C, D] overlap if A <= D and B >= C
            overlapping = qs.filter(
                lower_range__lte=upper_range,
                upper_range__gte=lower_range
            )
            if overlapping.exists():
                conflicts = [
                    f"'{rec.level}' ({rec.net_id}: {rec.lower_range:,.2f} - {rec.upper_range:,.2f})"
                    for rec in overlapping
                ]
                errors['non_field_errors'] = [
                    f"Range [{lower_range:,.2f} - {upper_range:,.2f}] overlaps with existing active level(s): {', '.join(conflicts)}."
                ]

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            user_header = request.headers.get('X-User-Name') or request.headers.get('X-User-Role')
            if user_header and not validated_data.get('created_user'):
                validated_data['created_user'] = user_header

        # Ensure NET_ID generation
        if not validated_data.get('net_id'):
            validated_data['net_id'] = MiNetGrowthLevel.generate_next_net_id()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request:
            user_header = request.headers.get('X-User-Name') or request.headers.get('X-User-Role')
            if user_header:
                validated_data['updated_user'] = user_header

        return super().update(instance, validated_data)
