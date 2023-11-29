from django import forms
from django.contrib import admin
from ccx_customizations.models import Origin, CustomCourseForEdXExtraData
from lms.djangoapps.ccx.models import CustomCourseForEdX

# CustomCourseForEdX Admin
class CustomCourseForEdXAdmin(admin.ModelAdmin):
    list_display = ('course_id','display_name', 'get_coach_display', 'get_coach2_display', 'structure_json') # Order fields inside the main (table) view
    search_fields = ('course_id', 'display_name', 'coach__username', 'coach2__username')
    raw_id_fields = ('coach','coach2')
    fields = ('course_id', 'display_name', 'coach', 'coach2', 'structure_json')  # Order fields inside the item view
    readonly_fields = ('course_id',)

    @admin.display(description='Coach Username')
    def get_coach_display(self, obj):
        return obj.coach.username if obj.coach else None

    @admin.display(description='Coach2 Username')
    def get_coach2_display(self, obj):
        return obj.coach2.username if obj.coach2 else None
    
    
# Origin Admin
class OriginAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Fields to display in the admin list view
    search_fields = ('name',)  # Fields to search in the admin


# CustomCourseForEdXExtraData Admin
class CustomCourseForEdXExtraDataAdmin(admin.ModelAdmin):
    list_display = ('get_ccx_display_name', 'get_origin_display_name', 'first_name', 'last_name', 'class_name', 'class_num', 'organization', 'year')
    search_fields = ('ccx_course__display_name', 'ccx_origin__name', 'first_name', 'last_name', 'class_name', 'organization')  # Ensure these point to the correct field names
    list_filter = ('ccx_origin', 'year', 'organization')
    readonly_fields = ('ccx_course', 'ccx_origin')
    fields = ('ccx_course', 'ccx_origin', 'first_name', 'last_name', 'class_name', 'class_num', 'organization', 'year')  # Define the order of fields for the item view
    
    @admin.display(description='CCX Display Name')
    def get_ccx_display_name(self, obj):
        return obj.ccx_course.display_name if obj.ccx_course else None  # Ensure that obj.ccx_course is not None

    @admin.display(description='Origin Display Name')
    def get_origin_display_name(self, obj):
        return obj.ccx_origin.name if obj.ccx_origin else None  # Ensure that obj.ccx_origin is not None

# Registering the models with the admin
admin.site.register(CustomCourseForEdX, CustomCourseForEdXAdmin)
admin.site.register(Origin, OriginAdmin)
admin.site.register(CustomCourseForEdXExtraData, CustomCourseForEdXExtraDataAdmin)