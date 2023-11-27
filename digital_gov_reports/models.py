from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import F, OuterRef, Subquery

# necesery models 
from django.conf import settings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from lms.djangoapps.certificates.models import GeneratedCertificate
from lms.djangoapps.courseware.models import StudentModule
from lms.djangoapps.grades.models import PersistentCourseGrade

class CampusilReportableCoursesDigital(models.Model):
    isReportable = models.BooleanField(default=False)
    course_overview = models.ForeignKey(CourseOverview, on_delete=models.CASCADE)
   
    def get_courses_to_report(days_config = 7):
        # one week is 7 (days). 
        days_config = int(configuration_helpers.get_value('DIGITAL_TIME_DELTA', settings.DIGITAL_TIME_DELTA))
        now = timezone.now()
        time_delta = now - timedelta(days = days_config)
        
        # Subquery to get the grade from PersistentCourseGrade
        grade_subquery = PersistentCourseGrade.objects.filter(
            user_id=OuterRef('student_id'),
            course_id=OuterRef('course_id')
        ).values(
            'percent_grade',
            'letter_grade'
        )  # Assume one grade per course per student
        reportableCourses_subquery = CampusilReportableCoursesDigital.objects.filter(
            course_overview_id=OuterRef('course_id'),
        ).annotate(
            end = F('course_overview__end'),
           display_name = F('course_overview__display_name')
        ).values(
            'isReportable',
            'end',
            "display_name"
        )     
        certificate_subquery = GeneratedCertificate.objects.filter(
            user_id=OuterRef('student_id'),
            course_id=OuterRef('course_id')
        ).values(
            'status',
            'download_url',
            'verify_uuid'
        )

        queryset = StudentModule.objects.filter(
            # Add your filter conditions here
        ).annotate(
            student_email=F('student__email'),
            student_first_name = F('student__first_name'),
            student_last_name = F('student__last_name'),
            _student_id=F('student_id'),
            _course_id=F('course_id'),
            course_grade_total=Subquery(grade_subquery.values('percent_grade')),
            course_latter_grade=Subquery(grade_subquery.values('letter_grade')),
            reportable_course=Subquery(reportableCourses_subquery.values('isReportable')),
            course_end_date=Subquery(reportableCourses_subquery.values('end')),
            course_display_name=Subquery(reportableCourses_subquery.values('display_name')),
            student_certificate_status= Subquery(certificate_subquery.values('status')),
            student_certificate_verify_uuid= Subquery(certificate_subquery.values('verify_uuid'))
        ).values(
            'student_email',
            'student_first_name',
            'student_last_name',
            '_student_id',
            '_course_id',
            'course_grade_total',
            'course_latter_grade',
            'reportable_course',
            'course_end_date',
            'course_display_name',
            'student_certificate_status',
            'student_certificate_verify_uuid'
        ).distinct()
        
        return queryset