from django.contrib.auth.models import Group
from users.models import User
from occuhunt.settings import LINKEDIN_CONSUMER_KEY, LINKEDIN_CONSUMER_SECRET
import oauth2 as oauth
import time, json

def create_password(request, backend, *args, **kwargs):
    user = kwargs['user']
    uid = kwargs['uid']
    user.linkedin_uid = uid
    user.set_password(uid)
    user.save()

def associate_group(request, backend, *args, **kwargs):
    try:
        print kwargs
        if type(kwargs['response']['educations']['education']) == type({}):
            if "University of California, Berkeley".lower() in kwargs['response']['educations']['education']['school-name'].lower():
                    g = Group.objects.get(name='UC Berkeley')
                    user = kwargs['user']
                    user.groups.add(g)
                    user.save()
        elif type(kwargs['response']['educations']['education']) == type([]):
            for education in kwargs['response']['educations']['education']:
                if "University of California, Berkeley".lower() in education['school-name'].lower():
                    g = Group.objects.get(name='UC Berkeley')
                    user = kwargs['user']
                    user.groups.add(g)
                    user.save()
    except Exception as e:
        print e

def get_connections(request, backend, *args, **kwargs):
    url = "http://api.linkedin.com/v1/people/~/connections?format=json"
    consumer = oauth.Consumer(key=LINKEDIN_CONSUMER_KEY, secret=LINKEDIN_CONSUMER_SECRET)
     
    access_token = kwargs['response']['access_token']
    oauth_token_secret = access_token[19:access_token.find("&oauth_token=")]
    oauth_token_key = access_token[access_token.find("&oauth_token=")+13:]
    token = oauth.Token(key=oauth_token_key, secret=oauth_token_secret)

    client = oauth.Client(consumer, token)

    resp, content = client.request(url)

