"""
API library for Django REST Framework permissions-oriented workflows
"""
from rest_framework.permissions import BasePermission
from common.djangoapps.student.roles import GlobalStaff
from openedx.core.lib.api.view_utils import validate_course_key
from org_customizations.models import OrganizationExtraData
from openedx.core.djangoapps.content.course_overviews.models import \
    CourseOverview
   

class IsOrgStaff(BasePermission):
    """
    Allows access to org staff members and global staff users. 

    Permission that checks whether the user is part of the above
    If none of those conditions are met, HTTP403 is returned.
    """

    def has_permission(self, request, view):
        
        if GlobalStaff().has_user(request.user):
            return True
        
        course_key_string = view.kwargs.get('course_id')
        course_key = validate_course_key(course_key_string)
        course_obj = CourseOverview.objects.get(id=course_key)
        org = course_obj.org
                    
        #Check if the user is a member of the course organization
        if OrganizationExtraData.objects.filter(org__name=org, api_user__username = request.user).exists():
           return True 
       

 