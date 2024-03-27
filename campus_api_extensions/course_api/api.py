"""
CampusIL Course API
"""
from common.djangoapps.student.models import CourseAccessRole
from common.djangoapps.student.roles import GlobalStaff
from django.contrib.auth.models import \
    User  # lint-amnesty, pylint: disable=imported-auth-user
from edx_django_utils.monitoring import function_trace
from lms.djangoapps.courseware.access import has_access
from opaque_keys.edx.django.models import CourseKeyField
from openedx.core.djangoapps.content.course_overviews.models import \
    CourseOverview
from openedx.core.lib.api.view_utils import LazySequence

from ..campus_roles import get_staff_orgs
from .permission import can_view_courses_for_username


def get_effective_user(requesting_user, target_username):
    """
    Get the user we want to view information on behalf of.
    """
    if target_username == requesting_user.username:
        return requesting_user
    
    elif can_view_courses_for_username(requesting_user, target_username):
        return User.objects.get(username=target_username)


@function_trace('list_course_keys')
def list_course_keys(request, username, role):
    """
    Yield all available CourseKeys for the user having the given role.

    The courses returned include those for which the user identified by
    `username` has the given role.  Additionally, the logged in user
    should be an organization staff member to view courses available to that
    user.

    Note: This function does not use branding to determine courses.

    Arguments:
        request (HTTPRequest):
            Used to identify the logged-in user and to instantiate the course
            module to retrieve the course about description
        username (string):
            The name of the user the logged-in user would like to be
            identified as

    Keyword Arguments:
        role (string):
            Course keys are filtered such that only those for which the
            user has the specified role are returned.

    Return value:
        Yield `CourseKey` objects representing the collection of courses.

    """
    user = get_effective_user(request.user, username)
    all_course_keys = CourseOverview.get_all_course_keys()
    
    # Logged in user who is a global staff is allowed to view all courses.
    if GlobalStaff().has_user(request.user):
        return all_course_keys
    
    if role == 'staff':
        # This short-circuit implementation bypasses has_access() which we think is too slow for some users when
        # evaluating staff-level course access for Insights.  Various tickets have context on this issue: CR-2487,
        # TNL-7448, DESUPPORT-416, and probably more.
        #
        # This is a simplified implementation that does not consider org-level access grants (e.g. when course_id is
        # empty).
        filtered_course_keys = (
            CourseAccessRole.objects.filter(
                user=user,
                # Having the instructor role implies staff access.
                role__in=['staff', 'instructor'],
            )
            # We need to check against CourseOverview so that we don't return any Libraries.
            .extra(tables=['course_overviews_courseoverview'], where=['course_id = course_overviews_courseoverview.id'])
            # For good measure, make sure we don't return empty course IDs.
            .exclude(course_id=CourseKeyField.Empty)
            .order_by('course_id')
            .values_list('course_id', flat=True)
            .distinct()
        )
    else:
        orgs_short_name = get_staff_orgs(request.user)
        filtered_course_keys = LazySequence(
            (
                course_key for course_key in all_course_keys
                if has_access(user, role, course_key) and course_key.org in orgs_short_name
            ),
            est_len=len(all_course_keys)
        )
    return filtered_course_keys
