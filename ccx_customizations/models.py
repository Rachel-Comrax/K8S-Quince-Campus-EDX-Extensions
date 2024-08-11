""" Campus Edx Extensions models """

from django.db import models
from lms.djangoapps.ccx.models import CustomCourseForEdX
        
class Origin(models.Model):
    '''
    Added new table for the CCX origin types.
    '''
    name = models.CharField(max_length=255, unique=True)
    
    class Meta:
        app_label = 'ccx_customizations'
        verbose_name = 'CCX Origin'
        verbose_name_plural = 'CCX Origins'
    
    def __str__(self):
        return self.name
        
class CustomCourseForEdX(models.Model):
    # This is a temporary stub. Define fields if necessary, or keep it empty.
    pass
        
class CustomCourseForEdXExtraData(models.Model):
    '''
    Added extension table for the CCX class extra data.
    '''
    ccx_course = models.OneToOneField(
        CustomCourseForEdX,
        on_delete=models.CASCADE,               # Defines what happens when the referenced object is deleted.
        related_name='ccx_extra_data'           # The name to use for the reverse relation from CustomCourseForEdX back to CustomCourseForEdXExtraData.
    )
    
    ccx_origin = models.ForeignKey(
        Origin,
        on_delete=models.CASCADE,               # Defines what happens when the referenced object is deleted.
        related_name='ccx_extra_data_origin'    # The name to use for the reverse relation from Origin back to CustomCourseForEdXExtraData.
    )
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    class_name = models.CharField(max_length=255)
    class_num = models.IntegerField()
    organization = models.CharField(max_length=255)
    year = models.CharField(max_length=50)
    
    class Meta:
        app_label = 'ccx_customizations'
        verbose_name = 'CCX Extra Data'
        verbose_name_plural = 'CCX Extra Data'
        
    def __str__(self):
        return self.ccx_course.display_name