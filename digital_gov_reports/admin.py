from django import forms
from django.contrib import admin
from .models import CampusilReportableCoursesDigital

class CampusilReportableCoursesDigitalAdminForm(forms.ModelForm):

    class Meta:
        model = CampusilReportableCoursesDigital
        fields = '__all__'


class CampusilReportableCoursesDigitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'isReportable', 'get_course_id', 'get_display_name', 'get_org',)
    search_fields = ('course_overview__display_name','course_overview__id','course_overview__org',)
    raw_id_fields = ('course_overview',)
    readonly_fields = ('get_display_name', 'get_org_name' ,'get_org',)
    form = CampusilReportableCoursesDigitalAdminForm
    #rename the orginal column names
    @admin.display(description='Display Name')
    def get_display_name(self, obj):
        return obj.course_overview.display_name
    
    @admin.display(description='Org name')
    def get_org_name(self, obj):
        return obj.course_overview.display_org_with_default

    @admin.display(description='Org')
    def get_org(self, obj):
        return obj.course_overview.org
    
    @admin.display(description='Course')
    def get_course_id(self, obj):
        return obj.course_overview_id
    
    def save_model(self, request, obj, form, change):
        # Check if a record with the same course_overview_id already exists
        existing_record = CampusilReportableCoursesDigital.objects.filter(course_overview_id=obj.course_overview_id).first()

        if existing_record:
            # If it exists, update the existing record
            existing_record.isReportable = obj.isReportable
            # Update the record in DB
            existing_record.save()
            return

        # If it doesn't exist, proceed with the regular save
        super().save_model(request, obj, form, change)


admin.site.register(CampusilReportableCoursesDigital, CampusilReportableCoursesDigitalAdmin)

