import logging
from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.db.models import OuterRef, Subquery

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from rest_framework import permissions  # lint-amnesty, pylint: disable=wrong-import-order
from rest_framework.generics import ListAPIView  # lint-amnesty, pylint: disable=wrong-import-order
from rest_framework.decorators import api_view
from social_django.models import UserSocialAuth

from common.djangoapps.student.models import CourseEnrollment
from common.djangoapps.util.disable_rate_limit import can_disable_rate_limit
from openedx.core.djangoapps.enrollments.paginators import CourseEnrollmentsApiListPagination
from openedx.core.djangoapps.enrollments.serializers import CourseEnrollmentsApiListSerializer
from openedx.core.djangoapps.enrollments.views import EnrollmentUserThrottle
from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
from openedx.core.lib.api.view_utils import DeveloperErrorViewMixin

from .permissions import IsOrgDataResearcher
from .forms import CourseEnrollmentsOrgApiListForm

log = logging.getLogger(__name__)

class CourseEnrollmentsOrgApiListSerializer(CourseEnrollmentsApiListSerializer):
    moe_idm = serializers.CharField()
    
    class Meta(CourseEnrollmentsApiListSerializer.Meta):
        fields = CourseEnrollmentsApiListSerializer.Meta.fields + ('moe_idm', )

@can_disable_rate_limit
class CourseEnrollmentsOrgApiListView(DeveloperErrorViewMixin, ListAPIView):
    """
        **Use Cases**

            Get a list of all course enrollments, optionally filtered by a course ID or list of usernames.

        **Example Requests**

            GET /api/enrollment/v1/enrollments

            GET /api/enrollment/v1/enrollments?course_id={course_id}

            GET /api/enrollment/v1/enrollments?username={username},{username},{username}

            GET /api/enrollment/v1/enrollments?course_id={course_id}&username={username}

            GET /api/enrollment/v1/enrollments?org={org_short_name}
            
        **Query Parameters for GET**

            * course_id: Filters the result to course enrollments for the course corresponding to the
              given course ID. The value must be URL encoded. Optional.

            * username: List of comma-separated usernames. Filters the result to the course enrollments
              of the given users. Optional.
              
            * org: Organization short name. Filters enrollment for a single organization only.

            * page_size: Number of results to return per page. Optional.

            * page: Page number to retrieve. Optional.

        **Response Values**

            If the request for information about the course enrollments is successful, an HTTP 200 "OK" response
            is returned.

            The HTTP 200 response has the following values.

            * results: A list of the course enrollments matching the request.

                * created: Date and time when the course enrollment was created.

                * mode: Mode for the course enrollment.

                * is_active: Whether the course enrollment is active or not.

                * user: Username of the user in the course enrollment.

                * course_id: Course ID of the course in the course enrollment.
                
                * org: Organization short name.

            * next: The URL to the next page of results, or null if this is the
              last page.

            * previous: The URL to the next page of results, or null if this
              is the first page.

            If the user is not logged in, a 401 error is returned.

            If the user is not global staff, a 403 error is returned.

            If the specified course_id is not valid or any of the specified usernames
            are not valid, a 400 error is returned.

            If the specified course_id does not correspond to a valid course or if all the specified
            usernames do not correspond to valid users, an HTTP 200 "OK" response is returned with an
            empty 'results' field.
    """
    authentication_classes = (
        JwtAuthentication,
        BearerAuthenticationAllowInactiveUser,
        SessionAuthenticationAllowInactiveUser,
    )
    permission_classes = (permissions.IsAuthenticated, IsOrgDataResearcher,)
    throttle_classes = (EnrollmentUserThrottle,)
    serializer_class = CourseEnrollmentsOrgApiListSerializer
    pagination_class = CourseEnrollmentsApiListPagination

    def get_queryset(self):
        """
        Get all the course enrollments for the given course_id and/or given list of usernames.
        """
        form = CourseEnrollmentsOrgApiListForm(self.request.query_params)
        if not form.is_valid():
            raise ValidationError(form.errors)

        queryset = CourseEnrollment.objects.all()
        course_id = form.cleaned_data.get('course_id')
        usernames = form.cleaned_data.get('username')
        org_short_name = form.cleaned_data.get('org_short_name')
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if usernames:
            queryset = queryset.filter(user__username__in=usernames)
        if org_short_name:
            queryset = queryset.filter(course__org=org_short_name)

        # Add IDM data to output in case user have it
        queryset = queryset.annotate(
            moe_idm=Subquery(
                UserSocialAuth.objects.filter(
                    user_id=OuterRef("user_id"),
                    provider='tpa-saml',
                    uid__startswith='moe-edu-idm:'
                ).values('uid')[:1]
            )
        )
    
        return queryset    
