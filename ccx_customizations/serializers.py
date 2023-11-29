""" CCX API v0 Serializers. """

from rest_framework import serializers
from lms.djangoapps.ccx.api.v0.serializers import CCXCourseSerializer
from ccx_customizations.models import CustomCourseForEdXExtraData

class CustomCourseForEdXExtraDataSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomCourseForEdXExtraData
    """
    ccx_course = CCXCourseSerializer(read_only=True)
    ccx_origin_name = serializers.CharField(source='ccx_origin.name', read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    class_name = serializers.CharField()
    class_num = serializers.IntegerField()
    organization = serializers.CharField()
    year = serializers.IntegerField()

    class Meta:
        model = CustomCourseForEdXExtraData
        fields = (
            'ccx_course',
            'ccx_origin_name',
            'first_name',
            'last_name',
            'class_name',
            'class_num',
            'organization',
            'year',
        )
        # For disambiguating within the drf-yasg swagger schema
        ref_name = 'ccx_customizations.CustomCourseForEdXExtraData'