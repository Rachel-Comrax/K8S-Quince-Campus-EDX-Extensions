"""
Common Django settings for campus_edx_extensions project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import unicode_literals

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'


# Application definition

INSTALLED_APPS = []

ROOT_URLCONF = 'campus_edx_extensions.urls'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True


# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OVERRIDE_API_CCX_ADD_CLASS_POST = 'campus_edx_extensions.campus_ac.overrides.post'
    settings.OVERRIDE_MARKETING_LINK = 'campus_edx_extensions.footer_customization.overrides.marketing_link'
    settings.OVERRIDE_IS_MARKETING_LINK_SET = 'campus_edx_extensions.footer_customization.overrides.is_marketing_link_set'
