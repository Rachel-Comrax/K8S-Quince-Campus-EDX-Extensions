#from .models import CampusilReportableCoursesDigital
import logging
from openedx.core.djangoapps.content.course_overviews.models import CampusilReportableCoursesDigital

log = logging.getLogger(__name__)

def get_digital_data_to_report():
    _queryset = CampusilReportableCoursesDigital.get_courses_to_report()
    _domain= 'http://localhost:18000/certificates/'
    _output = []  # Create an empty list to store the email values

    for row in _queryset:
        
        course_id_str = str(row["_course_id"])
        reportableCourses = None
       # course_end_strftime= row['course_end_date'].strftime("%Y-%m-%d")
        latter_grade =  1 if row["course_latter_grade"] == "Pass" else 0 
        # return 1 if student pass the course else 0 
        total_grade = "not attempt" if row["course_latter_grade"] is None else row["course_latter_grade"] 
        
        # 'not attempt' means if the student does not start the course yet
        certificate_status = "not attempt" if row['student_certificate_status'] is None else row['student_certificate_status']
        concat_certificate_url = str(_domain) + str(row['student_certificate_verify_uuid'])
        certificate_url = "not attempt" if row['student_certificate_verify_uuid'] is None else concat_certificate_url
          
        #log.info(f'student_last_name{row["student_last_name"]}')
        
        
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
            #"couese_end": course_end_strftime,
            "studant_meta": student
        }
        
        _output.append(fields_value)
        

    return _output