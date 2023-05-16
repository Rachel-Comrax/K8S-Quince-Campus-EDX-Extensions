"""
App configuration for campus_edx_extensions.
"""

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import (
    ProjectType, SettingsType, PluginSettings
)


EXTENSIONS_APP_NAME = 'google_recaptcha'


class GoogleReCaptcha(AppConfig):
    """
    Campus course import configuration.
    """
    name = EXTENSIONS_APP_NAME
    verbose_name = 'Google reCaptcha'

    # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {
        PluginSettings.CONFIG: {
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            },
            
            ProjectType.LMS: {                
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
        }
    }
    }
