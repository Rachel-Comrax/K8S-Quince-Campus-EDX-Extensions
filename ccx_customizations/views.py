""" API v0 views. """


import datetime
import json
import logging

import pytz
from ccx_keys.locator import CCXLocator
from django.contrib.auth.models import User  # lint-amnesty, pylint: disable=imported-auth-user
from django.db import transaction
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.djangoapps.ccx.models import CustomCourseForEdX
from lms.djangoapps.ccx.overrides import override_field_for_ccx
from lms.djangoapps.ccx.utils import add_master_course_staff_to_ccx, assign_staff_role_to_ccx
from lms.djangoapps.instructor.enrollment import enroll_email, get_email_params
from openedx.core.lib.api import authentication, permissions
from xmodule.modulestore.django import SignalHandler  # lint-amnesty, pylint: disable=wrong-import-order

from lms.djangoapps.ccx.api.v0.paginators import CCXAPIPagination
from lms.djangoapps.ccx.api.v0.serializers import CCXCourseSerializer

from lms.djangoapps.ccx.api.v0.views import get_valid_course, get_valid_input, valid_course_modules, make_user_coach

log = logging.getLogger(__name__)
TODAY = datetime.datetime.today  # for patching in tests

class CCXListViewCustomizations(GenericAPIView):
    """
        **Use Case**

            * Get the list of CCX courses for a given master course.

            * Creates a new CCX course for a given master course.

        **Example Request**

            GET /api/ccx/v0/ccx/?master_course_id={master_course_id}

            POST /api/ccx/v0/ccx {

                "master_course_id": "course-v1:Organization+EX101+RUN-FALL2099",
                "display_name": "CCX example title",
                "coach_email": "john@example.com",
                "max_students_allowed": 123,
                "course_modules" : [
                    "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week1",
                    "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week4",
                    "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week5"
                ]

            }

        **GET Parameters**

            A GET request can include the following parameters.

            * master_course_id: A string representation of a Master Course ID. Note that this must be properly
                encoded by the client.

            * page: Optional. An integer representing the pagination instance number.

            * order_by: Optional. A string representing the field by which sort the results.

            * sort_order: Optional. A string (either "asc" or "desc") indicating the desired order.

        **POST Parameters**

            A POST request can include the following parameters.

            * master_course_id: A string representation of a Master Course ID.

            * display_name: A string representing the CCX Course title.

            * coach_email: A string representing the CCX owner email.

            * max_students_allowed: An integer representing he maximum number of students that
                can be enrolled in the CCX Course.

            * course_modules: Optional. A list of course modules id keys.

        **GET Response Values**

            If the request for information about the course is successful, an HTTP 200 "OK" response
            is returned with a collection of CCX courses for the specified master course.

            The HTTP 200 response has the following values.

            * results: a collection of CCX courses. Each CCX course contains the following values:

                * ccx_course_id: A string representation of a CCX Course ID.

                * display_name: A string representing the CCX Course title.

                * coach_email: A string representing the CCX owner email.

                * start: A string representing the start date for the CCX Course.

                * due: A string representing the due date for the CCX Course.

                * max_students_allowed: An integer representing he maximum number of students that
                    can be enrolled in the CCX Course.

                * course_modules: A list of course modules id keys.

            * count: An integer representing the total number of records that matched the request parameters.

            * next: A string representing the URL where to retrieve the next page of results. This can be `null`
                in case the response contains the complete list of results.

            * previous: A string representing the URL where to retrieve the previous page of results. This can be
                `null` in case the response contains the first page of results.

        **Example GET Response**

            {
                "count": 99,
                "next": "https://openedx-ccx-api-instance.org/api/ccx/v0/ccx/?course_id=<course_id>&page=2",
                "previous": null,
                "results": {
                    {
                        "ccx_course_id": "ccx-v1:Organization+EX101+RUN-FALL2099+ccx@1",
                        "display_name": "CCX example title",
                        "coach_email": "john@example.com",
                        "start": "2019-01-01",
                        "due": "2019-06-01",
                        "max_students_allowed": 123,
                        "course_modules" : [
                            "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week1",
                            "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week4",
                            "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week5"
                        ]
                    },
                    { ... }
                }
            }

        **POST Response Values**

            If the request for the creation of a CCX Course is successful, an HTTP 201 "Created" response
            is returned with the newly created CCX details.

            The HTTP 201 response has the following values.

            * ccx_course_id: A string representation of a CCX Course ID.

            * display_name: A string representing the CCX Course title.

            * coach_email: A string representing the CCX owner email.

            * start: A string representing the start date for the CCX Course.

            * due: A string representing the due date for the CCX Course.

            * max_students_allowed: An integer representing he maximum number of students that
                can be enrolled in the CCX Course.

            * course_modules: A list of course modules id keys.

        **Example POST Response**

            {
                "ccx_course_id": "ccx-v1:Organization+EX101+RUN-FALL2099+ccx@1",
                "display_name": "CCX example title",
                "coach_email": "john@example.com",
                "start": "2019-01-01",
                "due": "2019-06-01",
                "max_students_allowed": 123,
                "course_modules" : [
                    "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week1",
                    "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week4",
                    "block-v1:Organization+EX101+RUN-FALL2099+type@chapter+block@week5"
                ]
    }
    """
    authentication_classes = (
        JwtAuthentication,
        authentication.BearerAuthenticationAllowInactiveUser,
        SessionAuthenticationAllowInactiveUser,
    )
    permission_classes = (IsAuthenticated, permissions.IsMasterCourseStaffInstructor)
    serializer_class = CCXCourseSerializer
    pagination_class = CCXAPIPagination

    def get(self, request):
        """
        Gets a list of CCX Courses for a given Master Course.

        Additional parameters are allowed for pagination purposes.

        Args:
            request (Request): Django request object.

        Return:
            A JSON serialized representation of a list of CCX courses.
        """
        master_course_id = request.GET.get('master_course_id')
        master_course_object, master_course_key, error_code, http_status = get_valid_course(master_course_id)
        if master_course_object is None:
            return Response(
                status=http_status,
                data={
                    'error_code': error_code
                }
            )

        queryset = CustomCourseForEdX.objects.filter(course_id=master_course_key)
        order_by_input = request.query_params.get('order_by')
        sort_order_input = request.query_params.get('sort_order')
        if order_by_input in ('id', 'display_name'):
            sort_direction = ''
            if sort_order_input == 'desc':
                sort_direction = '-'
            queryset = queryset.order_by(f'{sort_direction}{order_by_input}')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return response

    def post(self, request):
        """
        Creates a new CCX course for a given Master Course.

        Args:
            request (Request): Django request object.

        Return:
            A JSON serialized representation a newly created CCX course.
        """
        master_course_id = request.data.get('master_course_id')
        master_course_object, master_course_key, error_code, http_status = get_valid_course(
            master_course_id,
            advanced_course_check=True
        )
        if master_course_object is None:
            return Response(
                status=http_status,
                data={
                    'error_code': error_code
                }
            )

        # validating the rest of the input
        valid_input, field_errors = get_valid_input(request.data)
        if field_errors:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'field_errors': field_errors
                }
            )

        try:
            # Retired users should effectively appear to not exist when
            # attempts are made to modify them, so a direct User model email
            # lookup is sufficient here.  This corner case relies on the fact
            # that we scramble emails immediately during user lock-out.  Of
            # course, the normal cases are that the email just never existed,
            # or it is currently associated with an active account.
            coach = User.objects.get(email=valid_input['coach_email'])
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'error_code': 'coach_user_does_not_exist'
                }
            )

        if valid_input.get('course_modules'):
            if not valid_course_modules(valid_input['course_modules'], master_course_key):
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'error_code': 'course_module_list_not_belonging_to_master_course'
                    }
                )
        # prepare the course_modules to be stored in a json stringified field
        course_modules_json = json.dumps(valid_input.get('course_modules'))

        with transaction.atomic():
            ccx_course_object = CustomCourseForEdX(
                course_id=master_course_object.id,
                coach=coach,
                display_name=valid_input['display_name'],
                structure_json=course_modules_json
            )
            ccx_course_object.save()

            # Make sure start/due are overridden for entire course
            start = TODAY().replace(tzinfo=pytz.UTC)
            override_field_for_ccx(ccx_course_object, master_course_object, 'start', start)
            override_field_for_ccx(ccx_course_object, master_course_object, 'due', None)

            # Enforce a static limit for the maximum amount of students that can be enrolled
            override_field_for_ccx(
                ccx_course_object,
                master_course_object,
                'max_student_enrollments_allowed',
                valid_input['max_students_allowed']
            )

            # Hide anything that can show up in the schedule
            hidden = 'visible_to_staff_only'
            for chapter in master_course_object.get_children():
                override_field_for_ccx(ccx_course_object, chapter, hidden, True)
                for sequential in chapter.get_children():
                    override_field_for_ccx(ccx_course_object, sequential, hidden, True)
                    for vertical in sequential.get_children():
                        override_field_for_ccx(ccx_course_object, vertical, hidden, True)

            # make the coach user a coach on the master course
            make_user_coach(coach, master_course_key)

            # pull the ccx course key
            ccx_course_key = CCXLocator.from_course_locator(
                master_course_object.id,
                str(ccx_course_object.id)
            )
            # enroll the coach in the newly created ccx
            email_params = get_email_params(
                master_course_object,
                auto_enroll=True,
                course_key=ccx_course_key,
                display_name=ccx_course_object.display_name
            )
            enroll_email(
                course_id=ccx_course_key,
                student_email=coach.email,
                auto_enroll=True,
                email_students=True,
                email_params=email_params,
            )
            # assign staff role for the coach to the newly created ccx
            assign_staff_role_to_ccx(ccx_course_key, coach, master_course_object.id)
            # assign staff role for all the staff and instructor of the master course to the newly created ccx
            add_master_course_staff_to_ccx(
                master_course_object,
                ccx_course_key,
                ccx_course_object.display_name,
                send_email=False
            )

        serializer = self.get_serializer(ccx_course_object)

        # using CCX object as sender here.
        responses = SignalHandler.course_published.send(
            sender=ccx_course_object,
            course_key=ccx_course_key
        )
        for rec, response in responses:
            log.info('Signal fired when course is published. Receiver: %s. Response: %s', rec, response)
        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data
        )