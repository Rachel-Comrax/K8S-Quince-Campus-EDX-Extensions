"""
Common Django settings for campus_edx_extensions project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import unicode_literals
from django.conf import settings


# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OVERRIDE_CHANGE_ACCESS = 'ccx_emails.overrides.change_access'
    settings.OVERRIDE_GET_EMAIL_PARAMS = 'ccx_emails.overrides.get_email_params'
    settings.OVERRIDE_ENROLL_EMAIL = 'ccx_emails.overrides.enroll_email'
    settings.OVERRIDE_ASSIGN_STAFF_ROLE_TO_CCX = 'ccx_emails.overrides.assign_staff_role_to_ccx'
