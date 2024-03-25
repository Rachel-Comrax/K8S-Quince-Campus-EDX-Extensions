"""campus_edx_extensions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# pylint: disable=unused-import

from django.conf import settings
from django.urls import re_path

from .course_api import views as courseApiView
from .course_live import views as courseLiveView
from .enrollments import views as enrollmentsView
from .grades import views as gradesView

urlpatterns = [
    re_path(r'^course_enrollments_org/?$', enrollmentsView.CourseEnrollmentsOrgApiListView.as_view(), name='course_enrollments_org'),
    re_path(fr'^course_grades_org/{settings.COURSE_ID_PATTERN}/$',gradesView.CourseGradesOrgView.as_view(),name='course_grades'),
    re_path(fr'^course_live/course/{settings.COURSE_ID_PATTERN}/$',courseLiveView.CourseLiveConfigurationView.as_view(),name='course_live'),
    re_path(fr'^course_live/providers/{settings.COURSE_ID_PATTERN}/$',courseLiveView.CourseLiveProvidersView.as_view(),name='live_providers'),
    re_path(r'^course_ids/', courseApiView.CourseIdListView.as_view(), name="course-id-list")
]

