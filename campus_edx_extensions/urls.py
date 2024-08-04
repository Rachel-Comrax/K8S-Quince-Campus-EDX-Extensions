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
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^course_recommendations/$', views.get_user_courses, name='user_reco'),
    re_path(r'^released_langs/', views.released_langs, name='released_langs'),
    re_path(r'^courses_for_report/$', views.all_courses_for_report, name='reportable_courses')
]
