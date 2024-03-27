""" CampusIL API v0 views. """
from edx_rest_framework_extensions.auth.jwt.authentication import \
    JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import \
    SessionAuthenticationAllowInactiveUser
from lms.djangoapps.grades.api import CourseGradeFactory
from lms.djangoapps.grades.rest_api.v1.utils import (
    CourseEnrollmentPagination, GradeViewMixin)
from lms.djangoapps.grades.rest_api.v1.views import bulk_course_grade_context
from openedx.core.lib.api.authentication import \
    BearerAuthenticationAllowInactiveUser
from openedx.core.lib.api.view_utils import (PaginatedAPIView, get_course_key,
                                             verify_course_exists)
from xmodule.modulestore.django import \
    modulestore  # lint-amnesty, pylint: disable=wrong-import-order

from . import permissions


class CourseGradesOrgView(GradeViewMixin, PaginatedAPIView):
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
    authentication_classes = (
        JwtAuthentication,
        BearerAuthenticationAllowInactiveUser,
        SessionAuthenticationAllowInactiveUser,
    )

    permission_classes = (permissions.JWT_RESTRICTED_APPLICATION_OR_USER_ACCESS,)

    pagination_class = CourseEnrollmentPagination

    required_scopes = ['grades:read']

    @verify_course_exists("Requested grade for unknown course {course}")
    def get(self, request, course_id=None):
        """
        Gets a course progress status.
        Args:
            request (Request): Django request object.
            course_id (string): URI element specifying the course location.
                                Can also be passed as a GET parameter instead.
        Return:
            A JSON serialized representation of the requesting user's current grade status.
        """
        username = request.GET.get('username')

        course_key = get_course_key(request, course_id)
      
        if username:
            # If there is a username passed, get grade for a single user
            with self._get_user_or_raise(request, course_key) as grade_user:
                return self._get_single_user_grade(grade_user, course_key)
        else:
            # If no username passed, get paginated list of grades for all users in course
            return self._get_user_grades(course_key)

    def _get_user_grades(self, course_key):
        """
        Get paginated grades for users in a course.
        Args:
            course_key (CourseLocator): The course to retrieve user grades for.

        Returns:
            A serializable list of grade responses
        """
        user_grades = []
        users = self._paginate_users(course_key)

        with bulk_course_grade_context(course_key, users):
            for user, course_grade, exc in CourseGradeFactory().iter(users, course_key=course_key):
                if not exc:
                    user_grades.append(self._serialize_user_grade(user, course_key, course_grade))

        return self.get_paginated_response(user_grades)
