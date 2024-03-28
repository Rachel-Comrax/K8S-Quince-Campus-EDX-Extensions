""" CampusIL Permission Flags """
from rest_framework.permissions import IsAuthenticated

from edx_rest_framework_extensions.permissions import _NOT_JWT_RESTRICTED_PERMISSIONS, _JWT_RESTRICTED_PERMISSIONS

from ..campus_roles import IsOrgStaff


JWT_RESTRICTED_APPLICATION_OR_USER_ACCESS = (
    IsAuthenticated &
    (_NOT_JWT_RESTRICTED_PERMISSIONS | _JWT_RESTRICTED_PERMISSIONS | IsOrgStaff)
)
