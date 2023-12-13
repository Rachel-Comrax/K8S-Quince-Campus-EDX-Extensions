import datetime
import json
import logging
import pytz

from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.contrib.auth.models import User
from lms.djangoapps.ccx.models import CustomCourseForEdX
from lms.djangoapps.ccx.overrides import override_field_for_ccx
from lms.djangoapps.ccx.utils import add_master_course_staff_to_ccx, assign_staff_role_to_ccx
from lms.djangoapps.ccx.api.v0.views import get_valid_input, get_valid_course, valid_course_modules, make_user_coach
from lms.djangoapps.instructor.enrollment import enroll_email, get_email_params
from openedx.core.djangoapps.django_comment_common.models import FORUM_ROLE_ADMINISTRATOR, assign_role
from openedx.core.djangoapps.django_comment_common.utils import seed_permissions_roles
from ccx_keys.locator import CCXLocator
from xmodule.modulestore.django import SignalHandler

log = logging.getLogger(__name__)

def post(base_func, self, request):
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
            start = datetime.datetime.today().replace(tzinfo=pytz.UTC)
            override_field_for_ccx(ccx_course_object, master_course_object, 'start', start)
            override_field_for_ccx(ccx_course_object, master_course_object, 'due', None)

            # Enforce a static limit for the maximum amount of students that can be enrolled
            override_field_for_ccx(ccx_course_object, master_course_object, 'max_student_enrollments_allowed', valid_input['max_students_allowed'])

            # Hide anything that can show up in the schedule
            hidden = 'visible_to_staff_only'
            for chapter in master_course_object.get_children():
                override_field_for_ccx(ccx_course_object, chapter, hidden, True)
                for sequential in chapter.get_children():
                    override_field_for_ccx(ccx_course_object, sequential, hidden, True)
                    for vertical in sequential.get_children():
                        override_field_for_ccx(ccx_course_object, vertical, hidden, True)
            
            ccx_id = CCXLocator.from_course_locator(master_course_object.id, str(ccx_course_object.id))

            # Create forum roles
            seed_permissions_roles(ccx_id)
            # Assign administrator forum role to CCX coach
            assign_role(ccx_id, coach, FORUM_ROLE_ADMINISTRATOR)
    
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
