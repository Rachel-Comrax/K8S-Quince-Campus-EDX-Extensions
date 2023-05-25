"""
App configuration for campus_edx_extensions.
"""

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import (
    ProjectType, SettingsType, PluginSettings, PluginContexts
)


EXTENSIONS_APP_NAME = 'incomplete_profile_message'


class IncompleteProfileMessageConfig(AppConfig):
    """
    Incomplete Profile Message plugin configuration
    """
    name = EXTENSIONS_APP_NAME
    verbose_name = 'Incomplete Profile Message'

    # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {
        PluginSettings.CONFIG: {
            ProjectType.LMS: {                
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            },
        },
        PluginContexts.CONFIG: {
            'lms.djangoapp': {
                "course_dashboard": 'incomplete_profile_message.context_utils.incomplete_profile_message_context',
            },
        },
    }
