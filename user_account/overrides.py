from django.utils.translation import ugettext as _
from django.core.validators import ValidationError, validate_email
from common.djangoapps.student.models import email_exists_or_retired

def validate_new_email(base_func, user, new_email):
    """
    Given a new email for a user, does some basic verification of the new address If any issues are encountered
    with verification a ValueError will be thrown.
    """
    base_func(user, new_email)

    if email_exists_or_retired(new_email):
        raise ValueError(
            _(
                u"It looks like {new_email} belongs to an existing account. Try again with a different email address."
            ).format(new_email=new_email)
        )