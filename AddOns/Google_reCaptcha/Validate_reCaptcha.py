import requests
from django.conf import settings
from openedx.core.djangoapps.user_authn.exceptions import AuthFailedError
from django.utils.translation import ugettext as _

def validate_recaptcha(token):
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': str(settings.GOOGLE_RECAPTCHA_SERVER_SIDE_KEY),
        'response': token
    })
    response_dict = response.json()
    if not response_dict['success']:
        raise AuthFailedError (_("The answer you've entered is incorrect. Please try again"))
    return response.json()['success']