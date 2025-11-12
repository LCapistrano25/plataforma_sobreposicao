from django.contrib import admin
from .models import ZoningArea, PhytoecologyArea, EnvironmentalProtectionArea
# Register your models here.

class EnvironmentalProtectionAreaAdmin(admin.ModelAdmin):
    list_display = ('unit_name', 'domains', 'class_group', 'legal_basis', 'hash_id')
    search_fields = ('unit_name', 'domains', 'class_group')

    fieldsets = (
        (None, {
            'fields': ('unit_name', 'domains', 'class_group', 'legal_basis', 'hash_id', 'geometry'),
        }),
        ('Controle', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'hash_id')

admin.site.register(EnvironmentalProtectionArea, EnvironmentalProtectionAreaAdmin)