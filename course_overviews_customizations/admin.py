
from django.contrib import admin
from .models import  CourseOverview_Origin


class CourseOverview_OriginAdmin(admin.ModelAdmin): 

    pass




admin.site.register(CourseOverview_Origin, CourseOverview_OriginAdmin)