import logging

from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from tastypie.authentication import Authentication
from users.models import User

import provider.oauth2
from provider.oauth2.models import AccessToken
from django.contrib.sessions.models import Session

"""
This is a simple OAuth 2.0 authentication model for tastypie

Copied nearly verbatim from amrox's example 
 - https://github.com/amrox/django-tastypie-two-legged-oauth

Dependencies: 
 - django-oauth2-provider: https://github.com/caffeinehit/django-oauth2-provider

Example:
 - http://ianalexandr.com
"""

# stolen from piston
class OAuthError(RuntimeError):
    """Generic exception class."""
    def __init__(self, message='OAuth error occured.'):
        self.message = message

class OAuth20Authentication(Authentication):
    """
    OAuth authenticator. 

    This Authentication method checks for a provided HTTP_AUTHORIZATION
    and looks up to see if this is a valid OAuth Access Token
    """
    def __init__(self, realm='API'):
        self.realm = realm

    def is_authenticated(self, request, **kwargs):
        """
        Verify 2-legged oauth request. Parameters accepted as
        values in "Authorization" header, or as a GET request
        or in a POST body.
        """
        logging.info("OAuth20Authentication")

        try:
            key = request.GET.get('oauth_consumer_key')
            if not key:
                key = request.POST.get('oauth_consumer_key')
            if not key:
                auth_header_value = request.META.get('HTTP_AUTHORIZATION')
                if auth_header_value:
                    key = auth_header_value.split(' ')[1]
            if not key:
                logging.error('OAuth20Authentication. No consumer_key found.')
                return None
            """
            If verify_access_token() does not pass, it will raise an error
            """
            token = verify_access_token(key)

            # If OAuth authentication is successful, set the request user to the token user for authorization
            request.user = token.user

            # If OAuth authentication is successful, set oauth_consumer_key on request in case we need it later
            request.META['oauth_consumer_key'] = key
            return True
        except KeyError, e:
            logging.exception("Error in OAuth20Authentication.")
            request.user = AnonymousUser()
            return False
        except Exception, e:
            logging.exception("Error in OAuth20Authentication.")
            return False
        return True

def verify_access_token(key):
    # Check if key is in AccessToken key
    try:
        token = AccessToken.objects.get(token=key)

        # Check if token has expired
        if token.expires < timezone.now():
            raise OAuthError('AccessToken has expired.')
    except AccessToken.DoesNotExist, e:
        raise OAuthError("AccessToken not found at all.")

    logging.info('Valid access')
    return token

class SessionAuthentication(Authentication):
    """
    Authentication by using the session id

    This Authentication method checks for a provided HTTP_AUTHORIZATION
    and looks up to see if this is a vlid Session Token
    """
    def __init__(self, realm='API'):
        self.realm = realm

    def is_authenticated(self, request, **kwargs):
        """
        Verify session request. Parameters accepted as
        values in "Authorization" header, or as a GET request
        or in a POST body.
        """
        logging.info("SessionAuthentication")

        try:
            key = request.GET.get('session_key')
            if not key:
                key = request.POST.get('session_key')
            if not key:
                auth_header_value = request.META.get('HTTP_AUTHORIZATION')
                if auth_header_value:
                    key = auth_header_value.split(' ')[1]
            if not key:
                logging.error('SessionAuthentication. No session_key found.')
                return None
            """
            If verify_access_token() does not pass, it will raise an error
            """
            print key
            session = Session.objects.get(session_key=key)
            print session
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)

            request.user = user

            return True
        except KeyError, e:
            logging.exception("Error in SessionAuthentication.")
            request.user = AnonymousUser()
            return False
        except Exception, e:
            logging.exception("Error in OAuth20Authentication.")
            return False
        return True

class RecruiterAuthentication(Authentication):
    """
    Authentication by using the session id

    This Authentication method checks for a provided HTTP_AUTHORIZATION
    and looks up to see if this is a vlid Session Token
    """
    def __init__(self, realm='API'):
        self.realm = realm

    def is_authenticated(self, request, **kwargs):
        """
        Verify session request. Parameters accepted as
        values in "Authorization" header, or as a GET request
        or in a POST body.
        """
        logging.info("SessionAuthentication")

        try:
            key = request.GET.get('session_key')
            if not key:
                key = request.POST.get('session_key')
            if not key:
                auth_header_value = request.META.get('HTTP_AUTHORIZATION')
                if auth_header_value:
                    key = auth_header_value.split(' ')[1]
            if not key:
                logging.error('SessionAuthentication. No session_key found.')
                return None
            """
            If verify_access_token() does not pass, it will raise an error
            """
            session = Session.objects.get(session_key=key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)

            if user.is_recruiter or user.is_superuser:
                request.user = user
                return True
            else:
                return False
        except KeyError, e:
            logging.exception("Error in SessionAuthentication.")
            request.user = AnonymousUser()
            return False
        except Exception, e:
            logging.exception("Error in OAuth20Authentication.")
            return False
        return True