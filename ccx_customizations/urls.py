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
from django.urls import include, path, re_path

from ccx_customizations import views


CCX_URLS = ([
    path('', views.CCXListViewCustomizations.as_view(), name='list'),
], 'ccx')

app_name = 'v0'
urlpatterns = [
    path('ccx', include(CCX_URLS)),
]