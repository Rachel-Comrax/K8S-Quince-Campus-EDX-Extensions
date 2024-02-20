from django.contrib import admin
from .models import OrganizationExtraData, Vertical

# Vertical Admin
class VerticalAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    search_fields = ('name',)  
    
class OrganizationExtraDataAdmin(admin.ModelAdmin):
    list_display = ('org_name', 'org_short_name', 'heb_name', 'vertical_name')

    def org_name(self, obj):
        return obj.org.name
    org_name.short_description = 'Organization Name'
    
    def org_short_name(self, obj):
        return obj.org.short_name
    org_short_name.short_description = 'Organization Short Name'
    
    def vertical_name(self, obj):
    #returns all the related vertical object associated with the current organization instance
        return ' , '.join( v.name for v in obj.vertical.all())
    vertical_name.short_description = 'Verticals'
    
     
admin.site.register(Vertical, VerticalAdmin)
admin.site.register(OrganizationExtraData, OrganizationExtraDataAdmin)
