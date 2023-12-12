import logging
import os
import requests
import json
from datetime import datetime, timedelta
from django.conf import settings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

class ApiDigitalHubService(): 
    #Class-level variables/props
    __instance = None
    cache = None
    _certificate_path = "/edx/src/certificates/stage-certificate.pem"
    _cert_path = "/edx/src/certificates/stage-certificate.crt"
    _cert_key_path = "/edx/src/certificates/stage-private.key"

    if os.path.exists(_certificate_path):
         logging.info(f"File {_certificate_path} exists.")
    else:
        raise FileNotFoundError(f"File {_certificate_path} does not exist.")   
       
    @property
    def token(self):
        # Check if token is in cache and not expired
        if 'token' in self.cache and self.cache['expiry'] > datetime.now():
            logging.info(f'The token is: {self.cache["token"]}')
            return self.cache['token']
        # Token not found in cache or expired, refresh it
        token_expiration_minutes = int(configuration_helpers.get_value('DIGITAL_HUB_API_HOST_TOKEN_EXPIRATION', settings.DIGITAL_HUB_API_HOST_TOKEN_EXPIRATION))
        token = self.__refresh_token()
        # Assuming token expires in 1 hour
        expiry = datetime.now() + timedelta(minutes=token_expiration_minutes)  
        # Save the refreshed token and its expiry time in cache
        self.cache['token'] = token
        self.cache['expiry'] = expiry
        return token
    
    #Singleton instanse
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
    
    #%% Init section
    def __init__(self, cache = {}):
        self.cache = cache
     
        
    #%% Public section  
    def push_data(self, data = None, cert_path =_certificate_path):
          
        # Request headers
        headers = {
            "Authorization": f'{configuration_helpers.get_value("DIGITAL_HUB_API_HOST_TOKEN_TYPE", settings.DIGITAL_HUB_API_HOST_TOKEN_TYPE)} {self.token["access_token"]}',
            "client_id": configuration_helpers.get_value("DIGITAL_HUB_CLIENT_ID", settings.DIGITAL_HUB_CLIENT_ID),
            "client_secret": configuration_helpers.get_value("DIGITAL_HUB_CLIENT_SECRET", settings.DIGITAL_HUB_CLIENT_SECRET),
            "x-scope": configuration_helpers.get_value("DIGITAL_HUB_X_SCOPE", settings.DIGITAL_HUB_X_SCOPE)
        } 
                  
        # Endpoint URL
        endpoint = f'https://{configuration_helpers.get_value("DIGITAL_HUB_API_HOST_NAME", settings.DIGITAL_HUB_API_HOST_NAME)}/{configuration_helpers.get_value("DIGITAL_HUB_API_ENDPOINT_PUSH", settings.DIGITAL_HUB_API_ENDPOINT_PUSH)}'
        access_token = None

        try:
            # Send the request
            response = requests.post(endpoint, headers=headers, cert=(self._cert_path, self._cert_key_path), data=data)
              
            # Get the response data
            data = response.json()
            
            # Raise an exeption for 4** or 5** status code
            response.raise_for_status()          
            
            # Access the token
            access_token = data.get("access_token")     
            logging.info(f"Digital Hub: *** Success to push data! {response.status_code} ***")
                 
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Digital Hub: push data: *** HTTP error! \nException: {http_err} headers: {headers} certificate path: {cert_path}")
            raise http_err
                  
        return access_token   
    
    #%% Private section   
    def __refresh_token(self):
        response_data = {}
        # Request headers
        headers = {
            "Content-Type": configuration_helpers.get_value("DIGITAL_HUB_CONTENT_TYPE", settings.DIGITAL_HUB_CONTENT_TYPE),
        }
        
        # Endpoint URL
        endpoint = f'https://{configuration_helpers.get_value("DIGITAL_HUB_API_HOST_NAME", settings.DIGITAL_HUB_API_HOST_NAME)}/{configuration_helpers.get_value("DIGITAL_HUB_API_STATEMENTS_AUTH", settings.DIGITAL_HUB_API_STATEMENTS_AUTH)}'
        request_body = {
            "client_id": configuration_helpers.get_value("DIGITAL_HUB_CLIENT_ID", settings.DIGITAL_HUB_CLIENT_ID),
            "client_secret": configuration_helpers.get_value("DIGITAL_HUB_CLIENT_SECRET", settings.DIGITAL_HUB_CLIENT_SECRET),
             "scope": configuration_helpers.get_value("DIGITAL_HUB_X_SCOPE", settings.DIGITAL_HUB_X_SCOPE),
            "grant_type": configuration_helpers.get_value("DIGITAL_HUB_GRAND_TYPE", settings.DIGITAL_HUB_GRAND_TYPE)
        }
             
        try:
            # Send the request
            response = requests.post(endpoint, headers=headers, data=request_body)  
            # Raise an exeption for 4** or 5** status code
            response.raise_for_status()               
            # Get the response data
            response_data = response.json()
            logging.info(f"Digital-Hub: Auth Success! status code: {response.status_code} *** Response data: {response_data}  ***")
            
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Digital Hub: *** Auth Faild! HTTP error! Exception: {http_err} \n request body: {request_body} headers: {headers} ***")
            raise http_err
                          
        return response_data
    