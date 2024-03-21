from rest_framework.permissions import BasePermission

from common.djangoapps.student.roles import GlobalStaff, CourseDataResearcherRole
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.core.lib.api.view_utils import validate_course_key
from common.djangoapps.student.models import CourseEnrollment

class IsOrgDataResearcher(BasePermission):
    """
    Check if user is global or org's course staff

    Permission that checks to see if the user is global staff, course
    staff, course admin,If none of those conditions are met, HTTP403 is returned.
    """

    def has_permission(self, request, view):
        
        if GlobalStaff().has_user(request.user):
            return True
        
        # check provided courses for the Data Researcher role
        username = request.query_params.get('username')
        if username:
            username_enrollments = CourseEnrollment.objects.filter(user__username=username)
            
            for enrollment in username_enrollments:
                if CourseDataResearcherRole(enrollment.course_id).has_user(request.user):
                    return True
                
        # check provided courses for the Data Researcher role
        course_id = request.query_params.get('course_id')
        if course_id:
            course_key_string = course_id
            course_key = validate_course_key(course_key_string)
            return CourseDataResearcherRole(course_key).has_user(request.user)
        
        # check all org's courses for the Data Researcher role
        org_short_name = request.query_params.get('org_short_name')
        if org_short_name:
            queryset = CourseOverview.objects.filter(org=org_short_name)
            
            for course in queryset:
                if CourseDataResearcherRole(course.id).has_user(request.user):
                    return True
        
        return False
