""" Campus Edx Extensions models """

from django.db import models
from lms.djangoapps.ccx.models import CustomCourseForEdX
import json
from datetime import datetime

from ccx_keys.locator import CCXLocator
from django.contrib.auth.models import User  # lint-amnesty, pylint: disable=imported-auth-user
from django.db import models
from lazy import lazy
from opaque_keys.edx.django.models import CourseKeyField, UsageKeyField
from pytz import utc

from xmodule.error_block import ErrorBlock
from xmodule.modulestore.django import modulestore

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
    """
    A Custom Course.

    .. no_pii:
    """
    course_id = CourseKeyField(max_length=255, db_index=True)
    display_name = models.CharField(max_length=255)
    coach = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    coach2 = models.ForeignKey(User, related_name='ccx_coach2', null=True, blank=True, db_index=True, on_delete=models.SET_NULL, db_column='coach_id_2')
    # if not empty, this field contains a json serialized list of
    # the master course modules
    structure_json = models.TextField(verbose_name='Structure JSON', blank=True, null=True)

    class Meta:
        app_label = 'ccx'

    @lazy
    def course(self):
        """Return the CourseBlock of the course related to this CCX"""
        store = modulestore()
        with store.bulk_operations(self.course_id):
            course = store.get_course(self.course_id)
            if not course or isinstance(course, ErrorBlock):
                log.error("CCX {0} from {2} course {1}".format(  # pylint: disable=logging-format-interpolation
                    self.display_name, self.course_id, "broken" if course else "non-existent"
                ))
            return course

    @lazy
    def start(self):
        """Get the value of the override of the 'start' datetime for this CCX
        """
        # avoid circular import problems
        from .overrides import get_override_for_ccx
        return get_override_for_ccx(self, self.course, 'start')

    @lazy
    def due(self):
        """Get the value of the override of the 'due' datetime for this CCX
        """
        # avoid circular import problems
        from .overrides import get_override_for_ccx
        return get_override_for_ccx(self, self.course, 'due')

    @lazy
    def max_student_enrollments_allowed(self):
        """
        Get the value of the override of the 'max_student_enrollments_allowed'
        datetime for this CCX
        """
        # avoid circular import problems
        from .overrides import get_override_for_ccx
        return get_override_for_ccx(self, self.course, 'max_student_enrollments_allowed')

    def has_started(self):
        """Return True if the CCX start date is in the past"""
        return datetime.now(utc) > self.start

    def has_ended(self):
        """Return True if the CCX due date is set and is in the past"""
        if self.due is None:
            return False

        return datetime.now(utc) > self.due

    @property
    def structure(self):
        """
        Deserializes a course structure JSON object
        """
        if self.structure_json:
            return json.loads(self.structure_json)
        return None

    @property
    def locator(self):
        """
        Helper property that gets a corresponding CCXLocator for this CCX.

        Returns:
            The CCXLocator corresponding to this CCX.
        """
        return CCXLocator.from_course_locator(self.course_id, str(self.id))
    
    def _str_(self):
        return self.display_name
    
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