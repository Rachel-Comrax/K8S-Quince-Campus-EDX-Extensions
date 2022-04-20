"""
App configuration for campus_edx_extensions.
"""

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import (
    ProjectType, SettingsType, PluginSettings
)


EXTENSIONS_APP_NAME = 'course_import'


class CourseImportConfig(AppConfig):
    """
    Campus course import configuration.
    """
    name = EXTENSIONS_APP_NAME
    verbose_name = 'Course Import'

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
        }
    }
