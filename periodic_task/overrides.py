from common.djangoapps.student.models import CourseAccessRole
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
logger = get_task_logger(__name__)


def enrolled_students_features(base_func, course_key, features):
    """
    Helper method to give each person his role information.

    Saves the data of the person (student) and his attributes (features). 
    The function checks the role of the person, and put this information in the person's data (under the 'role' column),
    if the person does not have a role, his role will be 'Student'.

    """
    students = User.objects.filter(
        courseenrollment__course_id=course_key,
        courseenrollment__is_active=1,
    ).order_by('username').select_related('profile')
    students_list = base_func(course_key, features)
    
    
    for student in students:
        _id = student.id
        _student_dict = None
        for student_dict in students_list:
            if str(student_dict["id"]) == str(_id):
                _student_dict = student_dict
                break
        
        student_course_access_role = CourseAccessRole.objects.filter(
            user=student,
            course_id=course_key,
        )
        if student_course_access_role:
            _student_dict['role'] = student_course_access_role._result_cache[0].role
        else:
            _student_dict['role'] = 'Student'

    return students_list