from django.contrib import admin
from oauth2_provider.admin import AccessTokenAdmin
from oauth2_provider.models import get_access_token_model


class AccessTokenOverrideAdmin(AccessTokenAdmin):
    raw_id_fields = ("user", "source_refresh_token")


AccessToken = get_access_token_model()

admin.site.unregister(AccessToken)
admin.site.register(AccessToken, AccessTokenOverrideAdmin)
