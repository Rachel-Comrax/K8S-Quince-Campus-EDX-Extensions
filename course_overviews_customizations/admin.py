
from django.contrib import admin
from .models import CourseOverview_Origin


class CourseOverview_Origin_Admin(admin.ModelAdmin): 

    list_display = ('course_id_id','origin_id_id')




admin.site.register(CourseOverview_Origin, CourseOverview_Origin_Admin)