""" Campus Edx Extensions models """

from django.db import models
from django.contrib.auth.models import User

class WpCourseRecommendations(models.Model):
    """
    Two objects representing user object from user_auth table and recommendations array of specific user. 
    """
    user = models.OneToOneField(User, db_index=True, related_name="+", on_delete=models.CASCADE)
    recommendations = models.CharField(max_length=1000)

    @classmethod
    def get_recomdations_by_username(cls, username):
        return cls.objects.filter(user__username=username)
