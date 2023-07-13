import requests
from django.conf import settings
from django.utils.translation import ugettext as _
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangoapps.user_authn.exceptions import AuthFailedError


def validate_recaptcha(token):
    is_recaptcha_enabled = configuration_helpers.get_value(
        'IS_RECAPTCHA_ENABLED',
        settings.IS_RECAPTCHA_ENABLED
    )
    if not is_recaptcha_enabled:
        return True
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': str(settings.GOOGLE_RECAPTCHA_SERVER_SIDE_KEY),
        'response': token
    })
    response_dict = response.json()
    if not response_dict['success']:
        raise AuthFailedError (_("The answer you've entered is incorrect. Please try again"))
    return response.json()['success']
