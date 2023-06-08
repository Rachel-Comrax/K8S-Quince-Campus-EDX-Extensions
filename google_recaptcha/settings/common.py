"""
Common Django settings for course_import app.
"""
# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.

    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OVERRIDE_LOGIN_POST_GOOGLE_RECAPTCHA = 'google_recaptcha.overrides.login_post'
    settings.OVERRIDE_REGISTER_POST_GOOGLE_RECAPTCHA = 'google_recaptcha.overrides.register_post'
