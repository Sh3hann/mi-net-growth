import re
from decimal import Decimal
from django.db import models, transaction
from django.core.exceptions import ValidationError


class MiNetGrowthLevel(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    id = models.AutoField(primary_key=True, db_column='ID')
    net_id = models.CharField(max_length=20, unique=True, db_column='NET_ID', editable=False, blank=True)
    level = models.CharField(max_length=100, db_column='LEVEL')
    lower_range = models.DecimalField(max_digits=14, decimal_places=2, db_column='LOWER_RANGE')
    upper_range = models.DecimalField(max_digits=14, decimal_places=2, db_column='UPPER_RANGE')
    percentage = models.DecimalField(max_digits=6, decimal_places=2, db_column='PERCENTAGE')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE')
    created_user = models.CharField(max_length=100, default='SYSTEM', db_column='CREATED_USER')
    updated_date = models.DateTimeField(auto_now=True, db_column='UPDATED_DATE')
    updated_user = models.CharField(max_length=100, null=True, blank=True, db_column='UPDATED_USER')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', db_column='STATUS')
    attachment = models.FileField(upload_to='growth_attachments/%Y/%m/', null=True, blank=True, db_column='ATTACHMENT')
    comments = models.CharField(max_length=500, null=True, blank=True, db_column='COMMENTS')

    class Meta:
        db_table = 'SIA_MI_NET_GROWTH_LEVELS'
        verbose_name = 'MI Net Growth Level'
        verbose_name_plural = 'MI Net Growth Levels'
        ordering = ['lower_range', 'id']

    @classmethod
    def generate_next_net_id(cls):
        """
        Auto-generates sequential NET ID: NET001, NET002, NET003...
        Safely inspects existing records to avoid collisions even with deleted or custom numbers.
        """
        existing_ids = cls.objects.values_list('net_id', flat=True)
        max_num = 0
        for nid in existing_ids:
            if nid:
                match = re.search(r'NET(\d+)', str(nid), re.IGNORECASE)
                if match:
                    val = int(match.group(1))
                    if val > max_num:
                        max_num = val
        next_num = max_num + 1
        return f"NET{next_num:03d}"

    def clean(self):
        super().clean()
        
        # 1. Lower Range Validation
        if self.lower_range is not None and self.lower_range < Decimal('0'):
            raise ValidationError({'lower_range': 'LOWER_RANGE must be a non-negative number (>= 0).'})

        # 2. Upper Range > Lower Range Validation
        if self.lower_range is not None and self.upper_range is not None:
            if self.upper_range <= self.lower_range:
                raise ValidationError({
                    'upper_range': f'UPPER_RANGE ({self.upper_range}) must be strictly greater than LOWER_RANGE ({self.lower_range}).'
                })

        # 3. Percentage Limits Validation
        if self.percentage is not None:
            if self.percentage < Decimal('0') or self.percentage > Decimal('100'):
                raise ValidationError({'percentage': 'PERCENTAGE must be between 0.00% and 100.00%.'})

        # 4. Range Overlap Validation (for Active records)
        if self.status == 'Active' and self.lower_range is not None and self.upper_range is not None:
            overlapping_qs = MiNetGrowthLevel.objects.filter(status='Active').exclude(pk=self.pk)
            # Two ranges [A, B] and [C, D] overlap if A <= D and B >= C
            overlapping = overlapping_qs.filter(
                lower_range__lte=self.upper_range,
                upper_range__gte=self.lower_range
            )
            if overlapping.exists():
                conflicts = [
                    f"{o.net_id} - {o.level} [${o.lower_range:,.2f} to ${o.upper_range:,.2f}]"
                    for o in overlapping
                ]
                raise ValidationError({
                    'range_overlap': f"Range [{self.lower_range} - {self.upper_range}] overlaps with active record(s): {', '.join(conflicts)}"
                })

    def save(self, *args, **kwargs):
        if not self.net_id:
            self.net_id = self.generate_next_net_id()
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.net_id} ({self.level}) [{self.lower_range} - {self.upper_range}]"
