from django.contrib import admin
from .models import ZoningArea, PhytoecologyArea, EnvironmentalProtectionArea
# Register your models here.

class EnvironmentalProtectionAreaAdmin(admin.ModelAdmin):
    list_display = ('unit_name', 'domains', 'class_group', 'legal_basis', 'hash_id')
    search_fields = ('unit_name', 'domains', 'class_group')
    
    fieldsets = (
        (None, {
            'fields': ('unit_name', 'domains', 'class_group', 'legal_basis', 'hash_id', 'geometry')
        }),
    )
admin.site.register(EnvironmentalProtectionArea, EnvironmentalProtectionAreaAdmin)