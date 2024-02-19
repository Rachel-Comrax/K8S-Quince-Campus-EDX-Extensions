from django.db import models

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from ccx_customizations.models import Origin


class CourseOverviewExtraData(models.Model):
    course = models.ForeignKey(
        CourseOverview,
        on_delete=models.CASCADE,
        null = False,
        related_name = 'course_id'
    )
    origin = models.ManyToManyField(
        Origin, 
        null = False,
        related_name = 'origin_id'
    )

    class Meta:
        app_label = 'course_overviews_customizations'
        verbose_name = "Custom Course Overview"
        verbose_name_plural = "Custom Course Overviews"
        
    def __str__(self):
        # returns all the related origins object associated with the current courseoverview instance 
        return f"{self.course.display_name} course series:  {' , '.join( o.name for o in self.origin.all())}"
