from django.contrib import admin
from .models import OrganizationVerticals, Verticals

class OrganizationVertical_Admin(admin.ModelAdmin): 
    pass


# Vertical Admin
class VerticalAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    search_fields = ('name',)  

admin.site.register(Verticals, VerticalAdmin)
admin.site.register(OrganizationVerticals, OrganizationVertical_Admin)