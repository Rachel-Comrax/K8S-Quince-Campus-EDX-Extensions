import json
import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from common.djangoapps.student.roles import GlobalStaff
from openedx.core.djangoapps.lang_pref.api import released_languages
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from rest_framework.decorators import api_view
 
from campus_edx_extensions.models import WpCourseRecommendations
from digital_gov_reports.courses_report import get_digital_data_to_report

log = logging.getLogger(__name__)

@api_view(["GET"])
def get_user_courses(request):
    if not GlobalStaff().has_user(request.user):
        return HttpResponseForbidden("Must be {platform_name} staff to perform this action.".format(platform_name=settings.PLATFORM_NAME))
        
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


@api_view(["GET"])
def released_langs(request):
    language_list = []
    for code, name in released_languages():
        language_list.append({
            'code': code,
            'name': name,
            'released': True,
        })

    return JsonResponse(language_list, safe=False)

@api_view(["GET"])
def all_courses_for_report(request):
    if not GlobalStaff().has_user(request.user):
        return HttpResponseForbidden("Must be {platform_name} staff to perform this action.".format(platform_name=settings.PLATFORM_NAME))
        
    # Create a JSON response using JsonResponse
    _data = {"DIGITAL_TIME_DELTA": 10}
    _report_data = get_digital_data_to_report(**_data)
    _response_data = {
        "course_details": _report_data # Assuming you want to wrap the data in a "data" key
    }
   
    # Return the JSON response to the browser
    return JsonResponse(_response_data)
