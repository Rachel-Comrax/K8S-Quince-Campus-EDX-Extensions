from django.contrib import admin
from .models import CampusilReportableCoursesDigital
#from openedx.core.djangoapps.content.course_overviews.models import CampusilReportableCoursesDigital

class CampusilReportableCoursesDigitalAdmin(admin.ModelAdmin):
    
    def course_id(self,obj):
        return obj.courseoverview_ptr_id 
    
    list_display = [ 
        'course_id',
        'display_name', 
        'isReportable'
    ]
    
    fields = ('display_name', 'id', 'isReportable', 'org', 'display_org_with_default')
    
    readonly_fields = [
        'display_name',
        'id',
        'org',
        'display_org_with_default'
    ]
    
    search_fields = ['id']
    
       
admin.site.register(CampusilReportableCoursesDigital, CampusilReportableCoursesDigitalAdmin)
    