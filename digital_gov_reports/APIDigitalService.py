import logging
import requests
from datetime import datetime, timedelta
from django.conf import settings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from django.http import JsonResponse


class APIDigitalService(): 
 #%% Props / Vars section
    
    @property
    def token(self):
        # Check if token is in cache and not expired
        if 'token' in self.cache and self.cache['expiry'] > datetime.now():
            return self.cache['token']

        # Token not found in cache or expired, refresh it
        token_expiration_minutes = int(configuration_helpers.get_value('DIGITAL_API_HOST_TOKEN_EXPIRATION', settings.DIGITAL_API_HOST_TOKEN_EXPIRATION))
        token = self.__refresh_token()
        expiry = datetime.now() + timedelta(minutes=token_expiration_minutes)  # Assuming token expires in 1 hour

        # Save the refreshed token and its expiry time in cache
        self.cache['token'] = token
        self.cache['expiry'] = expiry

        return token
    
    #%% Init section

    def __init__(self, cache):
        self.cache = cache
    
    
    #%% Public section
    
    def push_data(self, data = None):
        # Request headers
        headers = {
            "Authorization": f'{configuration_helpers.get_value("DIGITAL_API_HOST_TOKEN_TYPE", settings.DIGITAL_API_HOST_TOKEN_TYPE)} {self.token}',
            "Content-Type": configuration_helpers.get_value("DIGITAL_API_HOST_STATEMENTS_CONTENT_TYPE", settings.DIGITAL_API_HOST_STATEMENTS_CONTENT_TYPE)
        }

        # Endpoint URL
        endpoint = f'https://{configuration_helpers.get_value("DIGITAL_API_HOST_NAME", settings.DIGITAL_API_HOST_NAME)}/{configuration_helpers.get_value("DIGITAL_API_HOST_STATEMENTS_URL", settings.DIGITAL_API_HOST_STATEMENTS_URL)}'

        try:
            # Send the request
            response = requests.post(endpoint, headers=headers, json=data)
            
            # Get the response data
            response_data = response.json()

            logging.info(f"Digital: Response data: {response_data}")
        except Exception as e:
            logging.error(f"Digital: Failed to send student courses data to Digital. Exception: {e}\nData: {data}")
        
        return response_data
    
    
    #%% Private section
    
    def __refresh_token(self):
       
        # Client ID and secret
        client_id = configuration_helpers.get_value("DIGITAL_API_HOST_CLIENT_ID", settings.DIGITAL_API_HOST_CLIENT_ID)
        client_secret = configuration_helpers.get_value("DIGITAL_API_HOST_CLIENT_SECRET", settings.DIGITAL_API_HOST_CLIENT_SECRET)

        # Request parameters
        token_type = configuration_helpers.get_value("DIGITAL_API_HOST_TOKEN_TYPE", settings.DIGITAL_API_HOST_TOKEN_TYPE)
        grant_type = configuration_helpers.get_value("DIGITAL_API_HOST_GRANT_TYPE", settings.DIGITAL_API_HOST_GRANT_TYPE)
        scope = configuration_helpers.get_value("DIGITAL_API_HOST_SCOPE", settings.DIGITAL_API_HOST_SCOPE)

        # Request headers
        headers = {
            "Content-Type": configuration_helpers.get_value("DIGITAL_API_HOST_TOKEN_CONTENT_TYPE", settings.DIGITAL_API_HOST_TOKEN_CONTENT_TYPE)
        }

        # Endpoint URL
        endpoint = f'https://{configuration_helpers.get_value("DIGITAL_API_HOST_NAME", settings.DIGITAL_API_HOST_NAME)}/{configuration_helpers.get_value("DIGITAL_API_HOST_TOKEN_URL", settings.DIGITAL_API_HOST_TOKEN_URL)}?grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&scope={scope}&token_type={token_type}'

        access_token = None
        try:
            # Send the request
            response = requests.post(endpoint, headers=headers)
            
            # Get the response data
            data = response.json()

            # Access the token
            access_token = data.get("access_token")
            
            #logging.info(f"Access token: {access_token}")
        except Exception as e:
            logging.info(f"Digtal: Failed to obtain access token. Exception: {e}")
        
        return access_token