import os
from decimal import Decimal
from django.db.models import Q, Max, Avg, Count
from django.http import FileResponse, Http404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import MiNetGrowthLevel
from .serializers import MiNetGrowthLevelSerializer


class MiNetGrowthLevelViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for MI Net Growth Levels.
    Endpoints:
    - POST   /api/mi-net-growth-levels/        (Create new record)
    - GET    /api/mi-net-growth-levels/        (List all records with search, filter, pagination)
    - GET    /api/mi-net-growth-levels/<id>/   (Retrieve single record)
    - PUT    /api/mi-net-growth-levels/<id>/   (Update full record)
    - PATCH  /api/mi-net-growth-levels/<id>/   (Partial update)
    - DELETE /api/mi-net-growth-levels/<id>/   (Delete record)
    - GET    /api/mi-net-growth-levels/statistics/ (Aggregate metrics for dashboard)
    - GET    /api/mi-net-growth-levels/<id>/download_attachment/ (Direct file download)
    """
    queryset = MiNetGrowthLevel.objects.all().order_by('lower_range', 'id')
    serializer_class = MiNetGrowthLevelSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 1. Status Filter: ?status=Active or ?status=Inactive
        status_param = self.request.query_params.get('status')
        if status_param and status_param.lower() in ['active', 'inactive']:
            queryset = queryset.filter(status__iexact=status_param)

        # 2. Search by Level, NET_ID, or Comments: ?search=xxx
        search_param = self.request.query_params.get('search')
        if search_param:
            queryset = queryset.filter(
                Q(level__icontains=search_param) |
                Q(net_id__icontains=search_param) |
                Q(comments__icontains=search_param)
            )

        # 3. Custom Ordering: ?ordering=percentage or -lower_range etc.
        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def list(self, request, *args, **kwargs):
        # Optional: support disabling pagination via ?paginate=false
        paginate_param = request.query_params.get('paginate')
        if paginate_param and paginate_param.lower() == 'false':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        return super().list(request, *args, **kwargs)

    def check_role_permissions(self, request, action_name):
        """
        Enforce Role-Based Access Control (RBAC):
        - CFO: Full access (Create, Read, Update, Delete)
        - DGM: Deputy General Manager (Create, Read, Update - No Delete)
        - RM : Relationship Manager (Read-Only)
        """
        role = request.headers.get('X-User-Role', '').upper()
        if not role:
            # Default to full permissions if not provided in header
            return None

        if role == 'RM' and action_name in ['create', 'update', 'partial_update', 'destroy']:
            return Response(
                {'detail': 'Permission Denied: Relationship Managers (RM) have Read-Only access.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if role == 'DGM' and action_name == 'destroy':
            return Response(
                {'detail': 'Permission Denied: Deputy General Managers (DGM) cannot delete records. Only CFO has delete privileges.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return None

    def create(self, request, *args, **kwargs):
        perm_error = self.check_role_permissions(request, 'create')
        if perm_error:
            return perm_error
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        perm_error = self.check_role_permissions(request, 'update')
        if perm_error:
            return perm_error
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        perm_error = self.check_role_permissions(request, 'partial_update')
        if perm_error:
            return perm_error
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        perm_error = self.check_role_permissions(request, 'destroy')
        if perm_error:
            return perm_error
        instance = self.get_object()
        net_id = instance.net_id
        level = instance.level
        self.perform_destroy(instance)
        return Response(
            {'message': f"Growth level '{net_id} - {level}' successfully deleted."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def download_attachment(self, request, pk=None):
        """
        Stream or download the attached document with proper Content-Disposition.
        """
        instance = self.get_object()
        if not instance.attachment or not instance.attachment.name:
            return Response({'detail': 'No attachment found for this record.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            file_path = instance.attachment.path
            file_name = os.path.basename(file_path)
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
            return response
        except FileNotFoundError:
            raise Http404("Attachment file does not exist on server storage.")

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Summary statistics for analytics dashboard cards.
        """
        all_levels = MiNetGrowthLevel.objects.all()
        total_count = all_levels.count()
        active_count = all_levels.filter(status='Active').count()
        inactive_count = all_levels.filter(status='Inactive').count()
        
        avg_percentage = all_levels.aggregate(avg=Avg('percentage'))['avg'] or 0.0
        max_upper_range = all_levels.aggregate(max_val=Max('upper_range'))['max_val'] or 0.0

        return Response({
            'total_levels': total_count,
            'active_levels': active_count,
            'inactive_levels': inactive_count,
            'avg_percentage': round(float(avg_percentage), 2),
            'max_upper_range': float(max_upper_range),
        })
