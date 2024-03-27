"""
CampusIL Course API Views
"""
from django.core.exceptions import ValidationError
from edx_django_utils.monitoring import function_trace
from lms.djangoapps.course_api.serializers import CourseKeySerializer
from lms.djangoapps.course_api.views import (CourseIdListUserThrottle,
                                             LazyPageNumberPagination)
from openedx.core.lib.api.view_utils import (DeveloperErrorViewMixin,
                                             view_auth_classes)
from rest_framework.generics import ListAPIView

from .api import list_course_keys
from .forms import CourseIdListGetForm


@view_auth_classes()
class CourseIdListView(DeveloperErrorViewMixin, ListAPIView):
    """
    **Use Cases**

        Request a list of course IDs for all courses the specified user can
        access based on the provided parameters.

    **Example Requests**

        GET /campus_api_extensions/courses_ids/

    **Response Values**

        Body comprises a list of course ids and pagination details.

    **Parameters**

        username (required):
            The username of the specified user whose visible courses we
            want to see.

        role (required):
            Course ids are filtered such that only those for which the
            user has the specified role are returned. Role can be "staff"
            or "instructor".
            Case-insensitive.

    **Returns**

        * 200 on success, with a list of course ids and pagination details
        * 400 if an invalid parameter was sent or the username was not provided
          for an authenticated request.
        * 403 if a user who does not have permission to masquerade as
          another user who specifies a username other than their own.
        * 404 if the specified user does not exist, or the requesting user does
          not have permission to view their courses.

        Example response:

            {
                "results":
                    [
                        "course-v1:edX+DemoX+Demo_Course"
                    ],
                "pagination": {
                    "previous": null,
                    "num_pages": 1,
                    "next": null,
                    "count": 1
                }
            }

    """
    class CourseIdListPageNumberPagination(LazyPageNumberPagination):
        max_page_size = 1000

    pagination_class = CourseIdListPageNumberPagination
    serializer_class = CourseKeySerializer
    throttle_classes = (CourseIdListUserThrottle,)

    @function_trace('get_queryset')
    def get_queryset(self):
        """
        Returns CourseKeys for courses which the user has the provided role.
        """
        form = CourseIdListGetForm(self.request.query_params, initial={'requesting_user': self.request.user})
 
        if not form.is_valid():
            raise ValidationError(form.errors)

        return list_course_keys(
            self.request,
            form.cleaned_data['username'],
            role=form.cleaned_data['role'],
        )

    @function_trace('paginate_queryset')
    def paginate_queryset(self, *args, **kwargs):
        """
        No-op passthrough function purely for function-tracing (monitoring)
        purposes.

        This should be called once per GET request.
        """
        return super().paginate_queryset(*args, **kwargs)

    @function_trace('get_paginated_response')
    def get_paginated_response(self, *args, **kwargs):
        """
        No-op passthrough function purely for function-tracing (monitoring)
        purposes.

        This should be called only when the response is paginated. Two pages
        means two GET requests and one function call per request. Otherwise, if
        the whole response fits in one page, this function never gets called.
        """
        return super().get_paginated_response(*args, **kwargs)

    @function_trace('filter_queryset')
    def filter_queryset(self, *args, **kwargs):
        """
        No-op passthrough function purely for function-tracing (monitoring)
        purposes.

        This should be called once per GET request.
        """
        return super().filter_queryset(*args, **kwargs)

    @function_trace('get_serializer')
    def get_serializer(self, *args, **kwargs):
        """
        No-op passthrough function purely for function-tracing (monitoring)
        purposes.

        This should be called once per GET request.
        """
        return super().get_serializer(*args, **kwargs)
