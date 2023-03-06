"""
Common Django settings for course_import app.
"""
import logging
LOGGER = logging.getLogger(__name__)


# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    LOGGER.info(f"we are here")
    """
    Set of plugin settings used by the Open Edx platform.

    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OVERRIDE_UPDATE_THIRD_PARTY_AUTH_CONTEXT_FOR_ENTERPRISE = 'password_expiration.overrides.update_third_party_auth_context_for_enterprise'
    settings.OVERRIDE_THIRD_PARTY_AUTH_CONTEXT = 'password_expiration.overrides.third_party_auth_context' # OVERRIDE_third_party_auth_context
