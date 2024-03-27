"""
View for course live app - customization to MOE partner
"""
from openedx.core.djangoapps.course_live.views import (
    CourseLiveConfigurationView as CourseLiveConfigurationViewBase,
    CourseLiveProvidersView as CourseLiveProvidersViewBase
) 

from ..campus_roles import IsOrgStaff


class CourseLiveConfigurationView(CourseLiveConfigurationViewBase):   
    """
    View for configuring CourseLive settings for Moe partner.
    """
    permission_classes = (IsOrgStaff,)

   
class CourseLiveProvidersView(CourseLiveProvidersViewBase):
    """
    Read only view that lists details of LIVE providers available for a course for Moe partner.
    """
    permission_classes = (IsOrgStaff,)

    
    