

from django.contrib import admin
from .models import  CourseOverviewExtraData

class CourseOverviewExtraDataAdmin(admin.ModelAdmin): 
    
    list_display = ('course__id','course__display_name', 'origin__name',)
    search_fields = ('course__display_name', 'origin__name')
    raw_id_fields = ('course', )

    def course__display_name(self, obj):
        return obj.course.display_name
    course__display_name.short_description = 'Course Display Name'
    
    def course__id(self, obj):
        return obj.course.id
    course__id.short_description = 'Course ID'

    def origin__name(self, obj):
    # returns all the related origins object associated with the current courseoverview instance 
        return ' , '.join( o.name for o in obj.origin.all())
    origin__name.short_description = "course series"

admin.site.register(CourseOverviewExtraData, CourseOverviewExtraDataAdmin)
