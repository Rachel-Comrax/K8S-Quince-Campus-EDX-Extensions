"""
Common Django settings for course_import app.
"""

from path import Path as path


# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.

    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    BASE_ROOT = path(__file__).abspath().dirname().dirname()
    settings.MAKO_TEMPLATE_DIRS_BASE += [BASE_ROOT / 'templates']
