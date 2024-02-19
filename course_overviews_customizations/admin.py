
from openedx.core.lib.courses import clean_course_id

from django.contrib import admin
from django import forms
from .models import  CourseOverviewExtraData

class CourseOverviewExtraDataAdmin(admin.ModelAdmin): 
    
    list_display = ('course_id','course_display_name', 'origins')
    search_fields = ('course__display_name', 'origin__name')
    raw_id_fields = ('course',)
    
    
    def course_display_name(self, obj):
        return obj.course.display_name
    course_display_name.short_description = 'Course Display Name'
    
    def course_id(self, obj):
        return obj.course.id
    course_id.short_description = 'Course ID'

    def origins (self, obj):
    # returns all the related origins object associated with the current courseoverview instance 
        return ' , '.join( o.name for o in obj.origin.all())
    origins.short_description = "course series"

    def clean_course_id(self):
        """
        Validate the course id
        """
        return clean_course_id(self)

admin.site.register(CourseOverviewExtraData, CourseOverviewExtraDataAdmin)