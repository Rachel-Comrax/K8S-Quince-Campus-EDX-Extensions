"""
Plugin context utils.
"""
from datetime import datetime
import pytz
import waffle

from django.urls import reverse

from common.djangoapps.edxmako.shortcuts import render_to_string

from common.djangoapps.student.models import UserProfile

from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers


def disclaimer_incomplete_fields_notification(user):
    """
    Get the list of fields that are considered as additional but required.
    If one of these fields are empty, then calculate the numbers of days
    between the joined date and the current day to decide whether to display or not
    the alert after a certain number of days passed from settings or site_configurations.
    """
    if not user.is_authenticated:
        return False

    days_passed_threshold = configuration_helpers.get_value(
        'DAYS_PASSED_TO_ALERT_PROFILE_INCOMPLETION',
        7,
    )
    user_profile = UserProfile.objects.get(user_id=user.id)
    joined = user_profile.user.date_joined
    current = datetime.now(pytz.utc)
    delta = current - joined

    if delta.days > days_passed_threshold:
        additional_fields = configuration_helpers.get_value(
            'FIELDS_TO_CHECK_PROFILE_COMPLETION',
            [],
        )
        for field_name in additional_fields:
            if not getattr(user_profile, field_name, None):
                return True

    return False


def incomplete_profile_message_context(context=None):
    """
    Show "incomplete profile message notification" if enabled
    """
    incomplete_profile_message = ''
    user = context.get('user')

    if (waffle.switch_is_active('enable_incomplete_profile_notification') and
            disclaimer_incomplete_fields_notification(user)):
        account_settings_link = reverse('account_settings')
        incomplete_profile_message = render_to_string(
            '_dashboard_incomplete_profile_notification.html',
            {'account_settings_link': account_settings_link},
        )
    return incomplete_profile_message
