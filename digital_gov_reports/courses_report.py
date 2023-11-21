from digital_gov_reports.models import CampusilReportableCoursesDigital
import logging
from openedx.core.lib.celery import APP
from django.conf import settings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

log = logging.getLogger(__name__)

def get_digital_data_to_report(**data):
#recive the outdata from data model
    _queryset = CampusilReportableCoursesDigital.get_courses_to_report()
#prepare the constant parametrs of certificare url
    _domain = configuration_helpers.get_value('LMS_ROOT_URL', settings.LMS_ROOT_URL)
    #_domain = _domain if _domain is not 'http://edx.devstack.lms:18000qwer1' else 'http://localhost:18000'  
    _prefix_certificate_url= f'{_domain}/certificates/'
#Create an empty list to store the element values 
    _output = []  
    _time_slot = data["DIGITAL_TIME_DELTA"]
    log.info(f'qwer10: DIGITAL_TIME_DELTA={_time_slot}')
    
    for row in _queryset:
#Adjust model properties to match product requirements
        course_id_str = str(row["_course_id"])
        course_end_strftime= None if row['course_end_date'] is None else row['course_end_date'].strftime("%Y-%m-%d")
# return 1 if student pass the course else 0 
        latter_grade =  1 if row["course_latter_grade"] == "Pass" else 0 
# the final grade in range of 0-100
        total_grade = None if row["course_grade_total"] is None else row["course_grade_total"] * 100   
# 'not attempt' means if the student has not started the course yet
        certificate_status = row['student_certificate_status']
#certificare url for download: 
        verify_uuid = row['student_certificate_verify_uuid'] 
        certificate_url = None if verify_uuid is None else _prefix_certificate_url + verify_uuid
     
# set the User info
        student = {
            "id": row["_student_id"],
            "first_name": row["student_first_name"],
            "last_name": str(row["student_last_name"]),
            "email": row["student_email"],
            "total_grade": total_grade,
            "pass": latter_grade,
            "certificate_status": certificate_status,
            "certificate_url": certificate_url    
        }
        
# set the output JSON with joined multiple tables data
        fields_value = {
            "course_id": course_id_str,
            "report_do_Digital": row["reportable_course"],
            "course_name": row["course_display_name"], 
            "couese_end": course_end_strftime,
            "studant_meta": student
        }
        _output.append(fields_value)
    return _output

@APP.task
def run_digital_data_to_report(**data):
    log.info('Digital data report execution has begun ')
    get_digital_data_to_report(**data)
    log.info('Digital data report execution end')
