from AddOns.Google_reCaptcha.Validate_reCaptcha import validate_recaptcha
from openedx.core.djangoapps.user_authn.exceptions import AuthFailedError
from common.djangoapps.util.json_request import JsonResponse
from common.djangoapps.student.helpers import get_next_url_for_login_page
from openedx.core.djangoapps.user_authn.cookies import set_logged_in_cookies
import logging
from openedx.core.djangoapps.user_authn.views.login import login_user
log = logging.getLogger("edx.student")

def login_post(prev_fn, self, request):
    """Log in a user.

    See `login_user` for details.

    Example Usage:

        POST /user_api/v1/login_session
        with POST params `email`, `password`.

        200 {'success': true}

    """
    
    try:
        reCaptcha_token = str(request.POST['recaptcha-validation-token'])
        validate_recaptcha(reCaptcha_token)
    except AuthFailedError as error:
        response_content = error.get_response()
        log.exception(response_content)
        response = JsonResponse(response_content, status=400)
        return response
    return login_user(request)

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
    data = request.POST.copy()
    self._handle_terms_of_service(data)
    try:
        reCaptcha_token = str(request.POST['recaptcha-validation-token'])
        validate_recaptcha(reCaptcha_token)
    except AuthFailedError:
        errors = {}
        errors['recaptcha-validation-token'] = [{"user_message":"The CAPTCHA you entered is incorrect. Please try again."}]
        return self._create_response(request, errors, status_code=400)

    response = self._handle_duplicate_email_username(request, data)
    if response:
        return response

    response, user = self._create_account(request, data)
    if response:
        return response

    redirect_url = get_next_url_for_login_page(request, include_host=True)
    response = self._create_response(request, {}, status_code=200, redirect_url=redirect_url)
    set_logged_in_cookies(request, response, user)
    return response