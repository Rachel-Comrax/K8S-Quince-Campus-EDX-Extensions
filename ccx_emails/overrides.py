import logging

from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.utils.html import strip_tags

from edx_ace import ace
from edx_ace.recipient import Recipient
from common.djangoapps.course_modes.models import CourseMode
from common.djangoapps.student.roles import CourseCcxCoachRole, CourseStaffRole
from common.djangoapps.student.models import (
    CourseEnrollment,
    CourseEnrollmentAllowed,
    is_email_retired
)
from common.djangoapps.util.json_request import JsonResponse
from lms.djangoapps.courseware.courses import get_course_with_access
from lms.djangoapps.instructor.views.tools import get_student_from_identifier
from lms.djangoapps.instructor.access import allow_access, ROLES, revoke_access
from lms.djangoapps.instructor.enrollment import EmailEnrollmentState
from lms.djangoapps.instructor.enrollment import enroll_email as base_enroll_email
from lms.djangoapps.instructor.enrollment import get_email_params as base_get_email_params
from lms.djangoapps.instructor.enrollment import send_mail_to_student as base_send_mail_to_student
from lms.djangoapps.instructor.message_types import (
    AccountCreationAndEnrollment, AddBetaTester, AllowedEnroll,
    AllowedUnenroll, EnrolledUnenroll, EnrollEnrolled,
    RemoveBetaTester
)
from lms.djangoapps.ccx.utils import ccx_course
from lms.djangoapps.ccx.models import CustomCourseForEdX
from lms.djangoapps.ccx.api.v0.views import make_user_coach
from openedx.core.djangoapps.ace_common.template_context import get_base_template_context
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangoapps.theming import helpers as theming_helpers
from openedx.core.djangolib.markup import Text

from opaque_keys.edx.keys import CourseKey
from ccx_emails.message_types import EnrollEnrolledCCXCoach, EnrollEnrolledCreateCCX
from ccx_keys.locator import CCXLocator

log = logging.getLogger(__name__)



def change_access(base_func, course, user, level, action, send_email=True):
    """
    Change access of user.

    `level` is one of ['instructor', 'staff', 'beta']
    action is one of ['allow', 'revoke']

    NOTE: will create a group if it does not yet exist.
    """

    try:
        role = ROLES[level](course.id)
    except KeyError:
        raise ValueError(u"unrecognized level '{}'".format(level))

    if action == 'allow':
        if level == 'ccx_coach':
            email_params = base_get_email_params(course, True)
            email_params['message_type'] = 'enrolled_enroll_ccx_coach'
            base_enroll_email(
                course_id=course.id,
                student_email=user.email,
                auto_enroll=True,
                email_students=send_email,
                email_params=email_params,
            )
        role.add_users(user)
    elif action == 'revoke':
        role.remove_users(user)
    else:
        raise ValueError(u"unrecognized action '{}'".format(action))


def enroll_email(base_func, course_id, student_email, auto_enroll=False, email_students=False, email_params=None, language=None):
    """
    Enroll a student by email.

    `student_email` is student's emails e.g. "foo@bar.com"
    `auto_enroll` determines what is put in CourseEnrollmentAllowed.auto_enroll
        if auto_enroll is set, then when the email registers, they will be
        enrolled in the course automatically.
    `email_students` determines if student should be notified of action by email.
    `email_params` parameters used while parsing email templates (a `dict`).
    `language` is the language used to render the email.

    returns two EmailEnrollmentState's
        representing state before and after the action.

    NOTE:
        enroll_email use a custom send_mail_to_student func which placed here!
    """
    previous_state = EmailEnrollmentState(course_id, student_email)
    enrollment_obj = None
    if previous_state.user and User.objects.get(email=student_email).is_active:
        # if the student is currently unenrolled, don't enroll them in their
        # previous mode

        # for now, White Labels use the
        # "honor" course_mode. Given the change to use "audit" as the default
        # course_mode in Open edX, we need to be backwards compatible with
        # how White Labels approach enrollment modes.
        if CourseMode.is_white_label(course_id):
            course_mode = CourseMode.HONOR
        else:
            course_mode = None

        if previous_state.enrollment:
            course_mode = previous_state.mode

        enrollment_obj = CourseEnrollment.enroll_by_email(student_email, course_id, course_mode)
        if email_students:
            if not email_params.get('message_type'):
                email_params['message_type'] = 'enrolled_enroll'
            email_params['email_address'] = student_email
            email_params['full_name'] = previous_state.full_name
            send_mail_to_student(base_send_mail_to_student, student_email, email_params, language=language)

    elif not is_email_retired(student_email):
        cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id=course_id, email=student_email)
        cea.auto_enroll = auto_enroll
        cea.save()
        if email_students:
            email_params['message_type'] = 'allowed_enroll'
            email_params['email_address'] = student_email
            send_mail_to_student(base_send_mail_to_student, student_email, email_params, language=language)

    after_state = EmailEnrollmentState(course_id, student_email)

    return previous_state, after_state, enrollment_obj


def get_email_params(base_func, course, auto_enroll, secure=True, course_key=None, display_name=None):
    email_params = base_func(course, auto_enroll, secure=secure, course_key=course_key, display_name=display_name)

    protocol = 'https' if secure else 'http'
    course_key = course_key or str(course.id)
    display_name = display_name or Text(course.display_name_with_default)
    ccx_auth = 'finish_auth?course_id='
    ccx_auto_reg_page = '/account/'
    ccx_enrollment_action = '&enrollment_action=enroll&email_opt_in=false'

    stripped_site_name = configuration_helpers.get_value(
        'SITE_NAME',
        settings.SITE_NAME
    )
    email_params['ccx_coach_dashboard'] = '{proto}://{site}{path}'.format(
        proto=protocol,
        site=stripped_site_name,
        path=reverse('ccx_coach_dashboard', kwargs={'course_id': course_key})
    )
    email_params['root_course_name'] = Text(course.display_name_with_default)

    ccx_auto_enroll_url = u'{proto}://{site}{page}{auth}{path}{action}'.format(
        proto=protocol,
        site=stripped_site_name,
        page=ccx_auto_reg_page,
        auth=ccx_auth,
        path=course_key,
        action=ccx_enrollment_action
    )
    email_params['ccx_auto_enroll_url'] = ccx_auto_enroll_url
    
    return email_params


def send_mail_to_student(base_func, student, param_dict, language=None):
    """
    Construct the email using templates and then send it.
    `student` is the student's email address (a `str`),

    `param_dict` is a `dict` with keys
    [
        `site_name`: name given to edX instance (a `str`)
        `registration_url`: url for registration (a `str`)
        `display_name` : display name of a course (a `str`)
        `course_id`: id of course (a `str`)
        `auto_enroll`: user input option (a `str`)
        `course_url`: url of course (a `str`)
        `email_address`: email of student (a `str`)
        `full_name`: student full name (a `str`)
        `message_type`: type of email to send and template to use (a `str`)
        `is_shib_course`: (a `boolean`)
    ]

    `language` is the language used to render the email. If None the language
    of the currently-logged in user (that is, the user sending the email) will
    be used.

    Returns a boolean indicating whether the email was sent successfully.
    """

    # Add some helpers and microconfig subsitutions
    if 'display_name' in param_dict:
        param_dict['course_name'] = param_dict['display_name']
    elif 'course' in param_dict:
        param_dict['course_name'] = Text(param_dict['course'].display_name_with_default)

    param_dict['site_name'] = configuration_helpers.get_value(
        'SITE_NAME',
        param_dict['site_name']
    )

    # Extract an LMS user ID for the student, if possible.
    # ACE needs the user ID to be able to send email via Braze.
    lms_user_id = 0
    if 'user_id' in param_dict and param_dict['user_id'] is not None and param_dict['user_id'] > 0:
        lms_user_id = param_dict['user_id']

    # Get required context
    site = theming_helpers.get_current_site()
    message_context = get_base_template_context(site)
    param_dict['logo_url'] = message_context["logo_url"]
    param_dict['homepage_url'] = message_context["homepage_url"]
    param_dict['dashboard_url'] = message_context["dashboard_url"]
    param_dict['platform_name'] = message_context["platform_name"]
    param_dict['platform_name_tag'] = message_context["platform_name_tag"]
    param_dict['contact_email'] = message_context["contact_email"]
    param_dict['support_contact_url'] = message_context["support_contact_url"]

    # see if there is an activation email template definition available as configuration,
    # if so, then render that
    message_type = param_dict['message_type']

    ace_emails_dict = {
        'account_creation_and_enrollment': AccountCreationAndEnrollment,
        'add_beta_tester': AddBetaTester,
        'allowed_enroll': AllowedEnroll,
        'allowed_unenroll': AllowedUnenroll,
        'enrolled_enroll': EnrollEnrolled,
        'enrolled_unenroll': EnrolledUnenroll,
        'remove_beta_tester': RemoveBetaTester,
        'enrolled_enroll_ccx_coach': EnrollEnrolledCCXCoach,
        'enrolled_enroll_create_ccx': EnrollEnrolledCreateCCX,
    }

    message_class = ace_emails_dict[message_type]
    message = message_class().personalize(
        recipient=Recipient(lms_user_id=lms_user_id, email_address=student),
        language=language,
        user_context=param_dict,
    )

    ace.send(message)


def assign_staff_role_to_ccx(base_func, ccx_locator, user, master_course_id):
    """
    Check if user has ccx_coach role on master course then assign them staff role on ccx only
    if role is not already assigned. Because of this coach can open dashboard from master course
    as well as ccx.
    :param ccx_locator: CCX key
    :param user: User to whom we want to assign role.
    :param master_course_id: Master course key
    """
    coach_role_on_master_course = CourseCcxCoachRole(master_course_id)
    # check if user has coach role on master course
    if coach_role_on_master_course.has_user(user):
        # Check if user has staff role on ccx.
        role = CourseStaffRole(ccx_locator)
        if not role.has_user(user):
            # assign user the staff role on ccx
            with ccx_course(ccx_locator) as course:
                allow_access(course, user, "staff", send_email=False)
                allow_access(course, user, "instructor", send_email=False)
                allow_access(course, user, "data_researcher", send_email=False)
                
                
def modify_access(base_func, request, course_id):
    course_id = CourseKey.from_string(course_id)
    course = get_course_with_access(
        request.user, 'instructor', course_id, depth=None
    )
    try:
        user = get_student_from_identifier(request.POST.get('unique_student_identifier'))
    except User.DoesNotExist:
        response_payload = {
            'unique_student_identifier': request.POST.get('unique_student_identifier'),
            'userDoesNotExist': True,
        }
        return JsonResponse(response_payload)

    # Check that user is active, because add_users
    # in common/djangoapps/student/roles.py fails
    # silently when we try to add an inactive user.
    if not user.is_active:
        response_payload = {
            'unique_student_identifier': user.username,
            'inactiveUser': True,
        }
        return JsonResponse(response_payload)

    rolename = request.POST.get('rolename')
    action = request.POST.get('action')
    if rolename not in ROLES:
        error = strip_tags(f"unknown rolename '{rolename}'")
        log.error(error)
        return HttpResponseBadRequest(error)

    # disallow instructors from removing their own instructor access.
    if rolename == 'instructor' and user == request.user and action != 'allow':
        response_payload = {
            'unique_student_identifier': user.username,
            'rolename': rolename,
            'action': action,
            'removingSelfAsInstructor': True,
        }
        return JsonResponse(response_payload)

    if action == 'allow':
        allow_access(course, user, rolename)
    elif action == 'revoke':
        revoke_access(course, user, rolename)
    else:
        return HttpResponseBadRequest(strip_tags(
            f"unrecognized action u'{action}'"
        ))

    if rolename == 'staff' and isinstance(course_id, CCXLocator):
        try:
            # Retrieve the CCX course using the CCX ID part of the course key
            ccx_id = course_id.ccx
            ccx_course = CustomCourseForEdX.objects.get(id=ccx_id)
            
            # Get the second coach case only
            if ccx_course.coach and ccx_course.coach.id != user.id:
                if action == 'allow':
                    # make the coach user a coach on the master course
                    coach_role_on_master_course = CourseCcxCoachRole(ccx_course.course_id)
                    coach_role_on_master_course.add_users(user)
                    # make user a second coach of the CCX course
                    ccx_course.coach2 = user
                    log.info(f'CampusIL: The CCX Class changes in roles. The {user.username} set as coach2.')
                elif action == 'revoke':
                    # remove user to be a second coach of the CCX course
                    if ccx_course.coach2.id == user.id:
                        ccx_course.coach2 = None
                    log.info(f'CampusIL: The CCX Class changes in roles. The {user.username} removed as coach2.')
                else:
                    return HttpResponseBadRequest(strip_tags(
                        f"unrecognized action u'{action}'"
                    ))
                ccx_course.save()
                
        except CustomCourseForEdX.DoesNotExist:
            # Handle the case where the CCX course does not exist
            ccx_course = None

    response_payload = {
        'unique_student_identifier': user.username,
        'rolename': rolename,
        'action': action,
        'success': 'yes',
    }
    return JsonResponse(response_payload)
    
