"""
App configuration for campus_edx_extensions.
"""

from __future__ import unicode_literals

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import (
    ProjectType, SettingsType, PluginSettings
)


EXTENSIONS_APP_NAME = 'periodic_task'


class PeriodicTaskConfig(AppConfig):
    """
    Campus EDX Extensions configuration.
    """
    name = EXTENSIONS_APP_NAME
    verbose_name = 'Periodic Task'

    # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {

        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
            },
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
            },
        }
    }
