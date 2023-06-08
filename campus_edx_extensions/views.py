import json
import logging

from django.conf import settings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from lms.djangoapps.mobile_api.decorators import mobile_view
from rest_framework.decorators import api_view


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import WpCourseRecommendations 


log = logging.getLogger(__name__)

@api_view(["GET"])
@mobile_view()
def get_user_courses(request):
      
      # initialization parameters
    _output = {"recomendations": None }
    _username = request.GET.get('user', request.user.username)
    _recomendationsRows = WpCourseRecommendations.get_recomdations_by_username(_username)

    # check that configuration key exist in yml
    if not hasattr(settings, "MIN_WEIGHT"):
        return JsonResponse({"errorMessage": "The MIN_WEIGHT is not set in yml configuration."})
    
    # check if the recommendations coll exists
    if _recomendationsRows.exists():
        _recomendationRow = _recomendationsRows[0]
        # extract the recommendations collection 
        _recomendations = json.loads(_recomendationRow.recommendations)
        # extract the weight valuse
        _minWeight = configuration_helpers.get_value('MIN_WEIGHT',settings.MIN_WEIGHT )
        # pick the recomendations that are greater than custom weight
        _relevant_recomendations = []
        for recomendation in _recomendations:
            if recomendation["weight"] >= _minWeight:
                _relevant_recomendations.append(recomendation)
         # sort the recommendations collection in ascending order       
        _sorted_recomendations = sorted(_relevant_recomendations, key=lambda x: x["weight"], reverse=True)
        # inject the new collection into the Json object
        _output["recomendations"] = [item["course_id"] for item in _sorted_recomendations]
    
    return (JsonResponse(_output))