from lms.djangoapps.courseware.tabs import DatesTab as DatesTabBase

class DatesTab(DatesTabBase):
    
    @classmethod
    def is_enabled(cls, course, user=None):
        return True
    
    @classmethod
    def is_hideable(cls, course, user=None):
        return True
    

