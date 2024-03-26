""" CampusIL Permission Flags """

from edx_rest_framework_extensions import permissions
from rest_framework.permissions import IsAuthenticated

from ..campus_roles import IsOrgStaff

_NOT_JWT_RESTRICTED_PERMISSIONS = permissions.NotJwtRestrictedApplication & (IsOrgStaff | permissions.IsUserInUrl)
JWT_RESTRICTED_APPLICATION_OR_USER_ACCESS = (
    IsAuthenticated &
    IsOrgStaff &
    (_NOT_JWT_RESTRICTED_PERMISSIONS | permissions._JWT_RESTRICTED_PERMISSIONS)
)
