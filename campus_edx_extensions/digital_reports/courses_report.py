#from .models import CampusilReportableCoursesDigital
from openedx.core.djangoapps.content.course_overviews.models import CampusilReportableCoursesDigital

def get_digital_data_to_report():
    _queryset = CampusilReportableCoursesDigital.get_courses_to_report()
    
    _output = []  # Create an empty list to store the email values
    
    # for row in _reportableCourses:
    #     reportableCourses = {
    #         "isReportable": row.isReportable
    #     }

    for row in _queryset:
        
        course_id_str = str(row["_course_id"])
        reportableCourses = None

        # get and set isReportable value

        reportableCourses = {
            "isReportable": row["reportable_course"]
        }
        
        # set the User info
        student = {
            "id": row["_student_id"],
            "email": row["student_email"]
        }
        
        # set the output JSON with joined multiple tables data
        fields_value = {
            "course_id": course_id_str,
            "course_grade_total": row["course_grade_total"],
            "course_report": reportableCourses,
            "course_student": student
        }
        
        _output.append(fields_value)
        

    return _output