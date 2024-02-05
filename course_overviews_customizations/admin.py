
from django.contrib import admin
from .models import  CourseOverview_Origin

class CourseOverview_OriginAdmin(admin.ModelAdmin): 
    list_display = ('course_id','course_display_name', 'origin_name')
    search_fields = ('course__display_name', 'origin__name')
    
    def course_display_name(self, obj):
        return obj.course.display_name
    course_display_name.short_description = 'Course Display Name'
    
    def course_id(self, obj):
        return obj.course.id
    course_id.short_description = 'Course ID'

    def origin_name(self, obj):
        return obj.origin.name
    origin_name.short_description = 'Origin Name'

admin.site.register(CourseOverview_Origin, CourseOverview_OriginAdmin)