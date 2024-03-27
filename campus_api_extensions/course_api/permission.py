"""
CampusIL Course API Authorization functions
"""

from common.djangoapps.student.roles import GlobalStaff

from ..campus_roles import is_org_staff


def can_view_courses_for_username(requesting_user, target_username):
    """
    Determine whether `requesting_user` has permission to view courses available
    to the user identified by `target_username`.

    Arguments:
        requesting_user (User): The user requesting permission to view another
        target_username (string):
            The name of the user `requesting_user` would like
            to access.

    Return value:
        Boolean:
            `True` if `requesting_user` is authorized to view courses as
            `target_username`.  Otherwise, `False`
    Raises:
        TypeError if target_username is empty or None.
    """

    # AnonymousUser is not allowed. 
    # logged-in user must insert a username
    if requesting_user.username == target_username:
        return True
    elif not target_username:
        raise TypeError("target_username must be specified")
    # Checking if the logged-in user has a custom role (organiztion staff)
    elif is_org_staff(requesting_user.username):
        return True       
    else:
        staff = GlobalStaff()
        return staff.has_user(requesting_user)
