from django.contrib import admin
from .models import OrganizationExtraData, OrganizationVerticals, Verticals

class OrganizationVertical_Admin(admin.ModelAdmin): 
    list_display = ('display_name',)
      
    def display_name(self, obj):
        return f"{obj.org.name} - {obj.vertical.name}"
    
    display_name.short_description = 'Organization - Vertical'

# Vertical Admin
class VerticalAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    search_fields = ('name',)  
    
class OrganizationExtraDataAdmin(admin.ModelAdmin):
    pass

admin.site.register(Verticals, VerticalAdmin)
admin.site.register(OrganizationVerticals, OrganizationVertical_Admin)
admin.site.register(OrganizationExtraData, OrganizationExtraDataAdmin)