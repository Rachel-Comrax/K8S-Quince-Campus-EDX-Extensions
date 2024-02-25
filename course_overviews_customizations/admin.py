

from django import forms
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from django.contrib import admin

from .models import  CourseOverviewExtraData

import logging 
log = logging.getLogger(__name__)


class CourseOverviewExtraDataForm(forms.ModelForm):
    """
    Premitive Custom Form Validation
    TODO: add customization on the UI 
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        if self.data.get('course'):
            try:
                self.data['course'] = CourseKey.from_string(self.data['course'])
            except InvalidKeyError:
                raise forms.ValidationError("No valid CourseKey for id {}!".format(self.data['course']))
            
    class Meta:
        fields = '__all__'
        model = CourseOverviewExtraData

@admin.register(CourseOverviewExtraData)
class CourseOverviewExtraDataAdmin(admin.ModelAdmin):   
    list_display = ('course__id','course__display_name', 'origin__name',)
    search_fields = ('course__display_name', 'origin__name',)
    raw_id_fields = ('course',)
    form = CourseOverviewExtraDataForm

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
    
