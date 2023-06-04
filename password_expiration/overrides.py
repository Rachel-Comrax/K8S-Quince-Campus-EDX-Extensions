"""
Utility methods for Enterprise
"""

from django.conf import settings
from django.utils.translation import ugettext as _
from common.djangoapps import third_party_auth
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangolib.markup import HTML, Text

import six
from django.contrib import messages

from common.djangoapps.third_party_auth import pipeline

import logging
LOGGER = logging.getLogger(__name__)

def update_third_party_auth_context_for_enterprise(prev_fn, request, context, enterprise_customer=None):
    LOGGER.info(f"override in here")
    """
    Return updated context of third party auth with modified for enterprise.

    Arguments:
        request (HttpRequest): The request for the logistration page.
        context (dict): Context for third party auth providers and auth pipeline.
        enterprise_customer (dict): data for enterprise customer

    Returns:
         context (dict): Updated context of third party auth with modified
         `errorMessage`.
    """
    

    if context['data']['third_party_auth']['errorMessage']:
        LOGGER.info(f"override in if")
        context['data']['third_party_auth']['errorMessage'] = Text(_(
            u'We are sorry, you are not authorized to access {platform_name} via this channel. '
            u'Please contact your learning administrator or manager in order to access {platform_name}.'
            u'{line_break}{line_break}'
            u'Error Details:{line_break}{error_message}{button_message}')
        ).format(
            platform_name=configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME),
            error_message=Text(_("Password expired. Please click here to reset your password.")),
            button_message = HTML("<button type='button' id='password-expire-url' href='#'>reset password</button>"),
            line_break=HTML('<br/>')
        )

    if enterprise_customer:
        context['data']['third_party_auth']['providers'] = []
        context['data']['third_party_auth']['secondaryProviders'] = []

    running_pipeline = third_party_auth.pipeline.get(request)
    if running_pipeline is not None:
        current_provider = third_party_auth.provider.Registry.get_from_pipeline(running_pipeline)
        if current_provider is not None and current_provider.skip_registration_form and enterprise_customer:
            # For enterprise (and later for everyone), we need to get explicit consent to the
            # Terms of service instead of auto submitting the registration form outright.
            context['data']['third_party_auth']['autoSubmitRegForm'] = False
            context['data']['third_party_auth']['autoRegisterWelcomeMessage'] = Text(_(
                'Thank you for joining {platform_name}. '
                'Just a couple steps before you start learning!')
            ).format(
                platform_name=configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME)
            )
            context['data']['third_party_auth']['registerFormSubmitButtonText'] = _('Continue')

    return context


def third_party_auth_context(prev_fn, request, redirect_to, tpa_hint=None):
    LOGGER.info(f"override in here2")
    """
    Context for third party auth providers and the currently running pipeline.

    Arguments:
        request (HttpRequest): The request, used to determine if a pipeline
            is currently running.
        redirect_to: The URL to send the user to following successful
            authentication.
        tpa_hint (string): An override flag that will return a matching provider
            as long as its configuration has been enabled

    Returns:
        dict

    """
    context = {
        "currentProvider": None,
        "providers": [],
        "secondaryProviders": [],
        "finishAuthUrl": None,
        "errorMessage": None,
        "registerFormSubmitButtonText": _("Create Account"),
        "syncLearnerProfileData": False,
        "pipeline_user_details": {}
    }

    if third_party_auth.is_enabled():
        for enabled in third_party_auth.provider.Registry.displayed_for_login(tpa_hint=tpa_hint):
            info = {
                "id": enabled.provider_id,
                "name": enabled.name,
                "iconClass": enabled.icon_class or None,
                "iconImage": enabled.icon_image.url if enabled.icon_image else None,
                "loginUrl": pipeline.get_login_url(
                    enabled.provider_id,
                    pipeline.AUTH_ENTRY_LOGIN,
                    redirect_url=redirect_to,
                ),
                "registerUrl": pipeline.get_login_url(
                    enabled.provider_id,
                    pipeline.AUTH_ENTRY_REGISTER,
                    redirect_url=redirect_to,
                ),
            }
            context["providers" if not enabled.secondary else "secondaryProviders"].append(info)

        running_pipeline = pipeline.get(request)
        if running_pipeline is not None:
            current_provider = third_party_auth.provider.Registry.get_from_pipeline(running_pipeline)
            user_details = running_pipeline['kwargs']['details']
            if user_details:
                context['pipeline_user_details'] = user_details

            if current_provider is not None:
                context["currentProvider"] = current_provider.name
                context["finishAuthUrl"] = pipeline.get_complete_url(current_provider.backend_name)
                context["syncLearnerProfileData"] = current_provider.sync_learner_profile_data

                if current_provider.skip_registration_form:
                    # As a reliable way of "skipping" the registration form, we just submit it automatically
                    context["autoSubmitRegForm"] = True

        # Check for any error messages we may want to display:
        for msg in messages.get_messages(request):
            try:
                if msg.extra_tags.split()[0] == "social-auth":
                    # msg may or may not be translated. Try translating [again] in case we are able to:
                    context["errorMessage"] = _(six.text_type(msg))  # pylint: disable=E7610
                    break
            except:
                context["errorMessage"] = _(six.text_type(msg))  # pylint: disable=E7610
                break               

    return context