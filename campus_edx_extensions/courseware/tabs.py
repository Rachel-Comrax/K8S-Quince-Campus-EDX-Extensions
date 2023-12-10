from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import gettext_noop
from lms.djangoapps.course_home_api.toggles import course_home_legacy_is_active
from openedx.features.course_experience.url_helpers import get_learning_mfe_home_url
from lms.djangoapps.courseware.tabs import DatesTab as DatesTabBase


class DatesTab(DatesTabBase):
    """
    A tab representing the relevant dates for a course.
    """
    type = "dates"
    # We don't have the user in this context, so we don't want to translate it at this level.
    title = gettext_noop("Dates")
    priority = 30
    view_name = "dates"
    is_hideable = True

    def __init__(self, tab_dict):
        def link_func(course, reverse_func):
            if course_home_legacy_is_active(course.id):
                return reverse_func(self.view_name, args=[str(course.id)])
            else:
                return get_learning_mfe_home_url(course_key=course.id, url_fragment=self.view_name)

        tab_dict['link_func'] = link_func
        super().__init__(tab_dict)
        
        # Default to hidden
        super().__init__({"is_hidden": True, **tab_dict})
        
    def to_json(self):
        json_val = super().to_json()
        # Persist that the tab is *not* hidden
        if not self.is_hidden:
            json_val.update({"is_hidden": False})
        return json_val
