"""
Setup file for campus_edx_extensions Django plugin.
"""

from __future__ import print_function

import os
import re

from setuptools import setup, find_packages


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split('#')[0].strip() for line in open(path).readlines()
            if is_requirement(line)
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, or editable.
    """
    # Remove whitespace at the start/end of the line
    line = line.strip()

    # Skip blank lines, comments, and editable installs
    return not (
        line == ''
        or line.startswith('-r')
        or line.startswith('#')
        or line.startswith('-e')
        or line.startswith('git+')
        or line.startswith('-c')
    )


def get_version(*file_paths):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


with open("README.rst", "r") as fh:
    README = fh.read()
  
VERSION = get_version('campus_edx_extensions', '__init__.py')
APP_NAMES_LMS = [
    "campus_edx_extensions = campus_edx_extensions.apps:CampusEdxExtensionsConfig",
    "ccx_emails = ccx_emails.apps:CCXEmailsConfig",
    "course_import = course_import.apps:CourseImportConfig",
    "workers_queue = workers_queue.apps:WorkersQueueConfig",
    "user_account = user_account.apps:UserAccountConfig",
    "periodic_task = periodic_task.apps:PeriodicTaskConfig",
    "video_transcripts = video_transcripts.apps:VideoTranscriptsConfig",
    "incomplete_profile_message = incomplete_profile_message.apps:IncompleteProfileMessageConfig",
    "google_recaptcha = google_recaptcha.apps:GoogleReCaptcha",
    "digital_gov_reports = digital_gov_reports.apps:DigitalReports",
    "ccx_customizations = ccx_customizations.apps:CCXCustomizations",
    "course_overviews_customizations = course_overviews_customizations.apps:CourseOverviewsCustomizations",
    "org_customizations = org_customizations.apps:OrgCustomizations",
    "campus_api_extensions = campus_api_extensions.apps:CampusApiExtensions",
    "explicit_queues = explicit_queues.apps:ExplicitQueuesConfig",
]
APP_NAMES_CMS = [
    "campus_edx_extensions = campus_edx_extensions.apps:CampusEdxExtensionsConfig",
    "course_import = course_import.apps:CourseImportConfig",
    "video_transcripts = video_transcripts.apps:VideoTranscriptsConfig",
]
TABS_NAMES = [
    "dates = campus_edx_extensions.courseware.tabs:DatesTab"
]


setup(
    name='campus_edx_extensions',
    version=VERSION,
    author='Raccoon Gang',
    author_email='contact@raccoongang.com',
    description='Campus EDX Extensions',
    license='AGPL',
    long_description=README,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(
        include=[
            'campus_edx_extensions*',
            'ccx_emails*',
            'course_import*',
            'workers_queue*',
            'video_transcripts*',
            'incomplete_profile_message*',
            'google_recaptcha*',
            'digital_gov_reports*',
            'ccx_customizations*',
            'course_overviews_customizations*',
            'org_customizations*',
            'campus_api_extensions*',
        ]),
    include_package_data=True,
    install_requires=load_requirements('requirements/base.in'),
    zip_safe=False,
    entry_points={"lms.djangoapp": APP_NAMES_LMS, "cms.djangoapp": APP_NAMES_CMS, "openedx.course_tab": TABS_NAMES })

