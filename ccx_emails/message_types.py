"""
ACE message types for the instructor module.
"""


from openedx.core.djangoapps.ace_common.message import BaseMessageType


class EnrollEnrolledCCXCoach(BaseMessageType):
    """
    A message for _registered_ learners who have been both invited and enrolled to a course.
    """
    APP_LABEL = 'ccx_emails'

    def __init__(self, *args, **kwargs):
        super(EnrollEnrolledCCXCoach, self).__init__(*args, **kwargs)
        self.options['transactional'] = True
