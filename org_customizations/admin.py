from django.contrib import admin
from .models import OrganizationExtraData, Vertical

# Vertical Admin
class VerticalAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    search_fields = ('name',)  
      
class OrganizationExtraDataAdmin(admin.ModelAdmin):
    list_display = ('org__name', 'org__short_name', 'heb_name', 'vertical__name','api_user__username',)
    search_fields = ('org__name', 'org__short_name',)  
    raw_id_fields = ('org', 'api_user',)

    def org__name(self, obj):
        return obj.org.name
    org__name.short_description = 'Organization Name'
    
    def org__short_name(self, obj):
        return obj.org.short_name
    org__short_name.short_description = 'Organization Short Name'
    
    def vertical__name(self, obj):
    #returns all the related vertical object associated with the current organization instance
        return ' , '.join( v.name for v in obj.vertical.all())
    vertical__name.short_description = 'Verticals'
    
    def api_user__username(self, obj):
    #returns all the related api users associated with the current organization 
        return ' , '.join( u.username for u in obj.api_user.all())
    api_user__username.username = 'Api Users'    
    
admin.site.register(Vertical, VerticalAdmin)
admin.site.register(OrganizationExtraData, OrganizationExtraDataAdmin)
