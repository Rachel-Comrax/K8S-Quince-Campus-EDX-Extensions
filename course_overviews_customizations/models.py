from django.db import models

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from ccx_customizations.models import Origin


class CourseOverview_Origin(models.Model):
    course = models.ForeignKey(
        CourseOverview,
        on_delete=models.PROTECT, # ensurre we can't delete a course if there are any origin associated with it
        null = False,
        related_name = 'course_id'
    )
    origin = models.ForeignKey(
        Origin, 
        on_delete=models.PROTECT, # ensurre we can't delete a origin if there are any course associated with it
        null = False,
        related_name = 'origin_id'
    )

    class Meta:
        app_label = 'course_overviews_customizations'
        verbose_name = "Course Overviews Origin"
        verbose_name_plural = "Course Overviews Origins"
        
    def __str__(self):
        return self.course.display_name
