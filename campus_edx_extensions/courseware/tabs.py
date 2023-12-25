from lms.djangoapps.courseware.tabs import DatesTab as DatesTabBase

class DatesTab(DatesTabBase):  
    is_hideable =  True
    
    def __init__(self, tab_dict):
        # After init, the tab is set to be hidden 
        super().__init__({"is_hidden": True, **tab_dict})
          

    def to_json(self):
        json_val = super().to_json()
        if not self.is_hidden:
        # Keep the tab 'is_not_hidden' after page refresh      
            json_val.update({"is_hidden": False})
        return json_val
