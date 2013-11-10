from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import os, time, simplejson, base64, urllib, hmac, sha
from string import strip
from django.http import Http404

from social_auth import __version__ as version
from social_auth.utils import setting

def resume_feed(request):
    """Resume feed view"""
    return render_to_response('resume_feed.html', {'version': version}, RequestContext(request))

def sign_s3_upload(request):
    AWS_ACCESS_KEY = 'AKIAJMUV3JF5IGAOPF3A'
    AWS_SECRET_KEY = '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'
    S3_BUCKET = 'resumefeed'

    object_name = request.GET['s3_object_name']
    mime_type = request.GET['s3_object_type']

    expires = int(time.time()+10)
    amz_headers = "x-amz-acl:public-read"

    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY,put_request, sha).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
    signed_request = '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature)

    json_results = simplejson.dumps({
        'signed_request': signed_request,
         'url': strip(url)
      })

    return HttpResponse(json_results, mimetype='application/json')

def submit_resume(request):
    resume_url = request.POST["resume_url"]
    return simplejson.dumps({
        'success': True
        })