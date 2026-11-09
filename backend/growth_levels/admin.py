from django.contrib import admin
from .models import MiNetGrowthLevel


@admin.register(MiNetGrowthLevel)
class MiNetGrowthLevelAdmin(admin.ModelAdmin):
    list_display = (
        'net_id',
        'level',
        'lower_range',
        'upper_range',
        'percentage',
        'status',
        'created_user',
        'created_date',
        'updated_date'
    )
    list_filter = ('status', 'created_date')
    search_fields = ('net_id', 'level', 'comments')
    readonly_fields = ('net_id', 'created_date', 'updated_date')
