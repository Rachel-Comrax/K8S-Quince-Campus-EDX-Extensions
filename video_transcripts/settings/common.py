"""
Common Django settings for course_import app.
"""


# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OVERRIDE_STUDIO_TRANSCRIPT = 'video_transcripts.overrides.studio_transcript'
