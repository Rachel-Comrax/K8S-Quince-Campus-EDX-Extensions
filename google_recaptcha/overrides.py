import logging

from common.djangoapps.util.json_request import JsonResponse
from django.utils.translation import ugettext as _
from openedx.core.djangoapps.user_authn.exceptions import AuthFailedError

from AddOns.Google_reCaptcha.Validate_reCaptcha import validate_recaptcha

log = logging.getLogger("edx.student")


def login_post(prev_fn, self, request, api_version):
    """Log in a user.

    See `login_user` for details.

    Example Usage:

        POST /user_api/v1/login_session
        with POST params `email`, `password`.

        200 {'success': true}

    """
    reCaptcha_token = request.POST.get('recaptcha-validation-token', False)
    if request.data['email'] == '' and request.data['password'] == '' and not reCaptcha_token:
        return prev_fn(self, request, api_version)
    try:
        reCaptcha_token = str(request.POST['recaptcha-validation-token'])
        validate_recaptcha(reCaptcha_token)
    except AuthFailedError as error:
        response_content = error.get_response()
        log.exception(response_content)
        response = JsonResponse(response_content, status=400)
        return response
    return prev_fn(self, request, api_version)


def register_post(prev_fn, self, request):
    """Create the user's account.

    You must send all required form fields with the request.

    You can optionally send a "course_id" param to indicate in analytics
    events that the user registered while enrolling in a particular course.

    Arguments:
        request (HTTPRequest)

    Returns:
        HttpResponse: 200 on success
        HttpResponse: 400 if the request is not valid.
        HttpResponse: 409 if an account with the given username or email
            address already exists
        HttpResponse: 403 operation not allowed
    """
    try:
        reCaptcha_token = str(request.POST['recaptcha-validation-token'])
        validate_recaptcha(reCaptcha_token)
    except AuthFailedError:
        errors = {}
        errors['recaptcha-validation-token'] = [{"user_message":_("The answer you've entered is incorrect. Please try again")}]
        return self._create_response(request, errors, status_code=400)

    return prev_fn(self, request)
