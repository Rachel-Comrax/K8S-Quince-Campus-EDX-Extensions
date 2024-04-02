""" CampusIL API v0 views. """
from lms.djangoapps.grades.rest_api.v1.views import CourseGradesView as CourseGradesViewBase

from . import permissions


class CourseGradesOrgView(CourseGradesViewBase):
    """
       **Use Case**
    
            Get course grades of all users who are enrolled in a course.
            The currently logged-in user requierd to be part of the api users list (Organization Customization)
            
        **Example Request**
        
            GET /campus_api_extensions/course_grades_org/{course_id}/                     - Get grades for all users in course
            GET /campus_api_extensions/{course_id}/?username={username}                   - Get grades for specific user in course    
    
        **GET Parameters**
        
            A GET request may include the following parameters.
            * course_id: (required) A string representation of a Course ID.
            * username:  (optional) A string representation of a user's username.
   
        **GET Response Values**
        
            If the request for information about the course grade
            is successful, an HTTP 200 "OK" response is returned.
            The HTTP 200 response has the following values.
            * username: A string representation of a user's username passed in the request.
            * email: A string representation of a user's email.
            * course_id: A string representation of a Course ID.
            * passed: Boolean representing whether the course has been
                    passed according to the course's grading policy.
            * percent: A float representing the overall grade for the course
            * letter_grade: A letter grade as defined in grading policy (e.g. 'A' 'B' 'C' for 6.002x) or None
  
        **Example GET Response**
        
            [{
                "username": "bob",
                "email": "bob@example.com",
                "course_id": "course-v1:edX+DemoX+Demo_Course",
                "passed": false,
                "percent": 0.03,
                "letter_grade": null,
            },
            {
                "username": "fred",
                "email": "fred@example.com",
                "course_id": "course-v1:edX+DemoX+Demo_Course",
                "passed": true,
                "percent": 0.83,
                "letter_grade": "B",
            },
            {
                "username": "kate",
                "email": "kate@example.com",
                "course_id": "course-v1:edX+DemoX+Demo_Course",
                "passed": false,
                "percent": 0.19,
                "letter_grade": null,
            }]
        """
    permission_classes = (permissions.JWT_RESTRICTED_APPLICATION_OR_USER_ACCESS,)
