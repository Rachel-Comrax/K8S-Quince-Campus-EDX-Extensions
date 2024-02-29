"""
Forms for validating user input to the Course Enrollment related views.
"""

from django.core.exceptions import ValidationError
from django.forms import CharField
from organizations.models import Organization
from openedx.core.djangoapps.enrollments.forms import CourseEnrollmentsApiListForm

import logging
log = logging.getLogger(__name__)

class CourseEnrollmentsOrgApiListForm(CourseEnrollmentsApiListForm):
    """
    A form that validates the query string parameters for the CourseEnrollmentsApiListView.
    """
    org_short_name = CharField(required=False)
    
    def clean_org_short_name(self):
        """
        Validate and return a course ID.
        """
        org_short_name = self.cleaned_data.get('org_short_name')
        
        if org_short_name:
            organization = Organization.objects.get(short_name=org_short_name)
            if organization is not None:
                return org_short_name
            else:
                raise ValidationError(f"'{org_short_name}' is not a valid org short name.")  # lint-amnesty, pylint: disable=raise-missing-from
