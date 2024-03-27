"""
Course API forms
"""
from django.forms import CharField, Form
from lms.djangoapps.course_api.forms import UsernameValidatorMixin


class CourseIdListGetForm(UsernameValidatorMixin, Form):
    """
    A form to validate query parameters in the course list retrieval endpoint
    """
    username = CharField(required=True)
    role = CharField(required=True)
