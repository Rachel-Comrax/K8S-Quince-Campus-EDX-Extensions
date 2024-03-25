"""
API library for Django REST Framework permissions-oriented workflows
"""
from common.djangoapps.student.roles import GlobalStaff
from openedx.core.djangoapps.content.course_overviews.models import \
    CourseOverview
from openedx.core.lib.api.view_utils import validate_course_key
from org_customizations.models import OrganizationExtraData
from rest_framework.permissions import BasePermission


class IsOrgStaff(BasePermission):
    """
    Allows access to organization staff members and global staff users. 

    Permission that checks whether the user is part of the above
    If none of those conditions are met, HTTP403 is returned.
    """

    def has_permission(self, request, view):
        
        if GlobalStaff().has_user(request.user):
            return True
        
        course_key_string = view.kwargs.get('course_id')
        course_key = validate_course_key(course_key_string)
        course_obj = CourseOverview.objects.get(id=course_key)
        org_short_name = course_obj.org
                       
        return is_org_staff(request.user, org_short_name)
     
def is_org_staff(username, org_short_name=None):  
    
    if org_short_name:
        return OrganizationExtraData.objects.filter(
            org__short_name=org_short_name, 
            api_user__username=username).exists()
    else:
        return OrganizationExtraData.objects.filter(
            api_user__username=username).exists()

def get_staff_orgs(username):
    orgs_qs =  OrganizationExtraData.objects.select_related('org').filter(api_user__username=username)
    staff_orgs = []
    for o in orgs_qs:
         staff_orgs.append(o.org.short_name) 
    return staff_orgs  
