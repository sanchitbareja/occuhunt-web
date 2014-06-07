# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os, time, simplejson, base64, urllib, hmac, sha, random, string
from string import strip
from django.http import Http404
from django.core import serializers

from documents.models import Document, Link, Visit

# Views
# 1. preview resume
# 2. view profile page

# API
# Document
# 1. Add a resume
# 2. Delete a resume
# 3. Get analytics
# 4. Get resumes for a user
# 5. 
# 
# Link
# 1. Add a link
# 2. Delete a link
# 3. Get analytics for links
# 4. Get links for a user
# 5. 

# Security concerns
# 1. resume should only be accessible by people I send it to
# 2. should not be able to directly download it from AWS s3 without a proper signature
# 3. should not be easily guessable and find the resume

@login_required
def profile_view(request):
	"""
	The main overview for a user to view all his documents (resumes, CVs, portfolio), links and analytics

	1. Get all resumes, CVs and portfolio links
	2. Get all links
	3. Get analytics for last 1 month
	4. 

	Corner Cases:
	1. No resumes/cvs/portfolio
	2. No links
	3. No analytics so far
	4. Too many data points for analytics
	5. Measure access times
	6. 
	"""
	resumes = Document.objects.filter(user=request.user, document_type=1, delete=False)
	cvs = Document.objects.filter(user=request.user, document_type=2, delete=False)
	portfolios = Document.objects.filter(user=request.user, document_type=3, delete=False)
	links = Link.objects.filter(user=request.user, delete=False)

	for resume in resumes:
		print resume.delete
		print resume.id
	data_to_send = {
		'resumes': resumes,
		'cvs': cvs,
		'portfolios': portfolios,
		'links': links
	}
	return render_to_response('profile/documents.html', data_to_send, RequestContext(request))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def preview_document(request, username, document_hash):
	"""
	Preview documents
	"""
	client_ip = get_client_ip(request)
	doc = Document.objects.filter(unique_hash=document_hash, delete=False)[0]
	links = Link.objects.filter(user__username=username, delete=False)
	if doc.user.username == username:
		data_to_send = {
			'document': doc,
			'links': links
		}
		return render_to_response('profile/preview.html', data_to_send, RequestContext(request))
	else:
		return render_to_response('profile/preview.html', data_to_send, RequestContext(request))

def individual_resume(request, hashstr):
    """Get individual resumes for sharing
    if resume exists: it should return page with just that resume
    else: it should give an error message saying that it does not exist.

    """
    print hashstr
    try:
        resume_url = "https://resumefeed.s3.amazonaws.com/"+str(hashstr)+""
        print resume_url
        unique_resume = Resume.objects.filter(url=resume_url)[0]
        print unique_resume
        print dir(unique_resume)
        unique_resume_comments = unique_resume.comment_set.all()
        serialized_comments = []
        for comment in unique_resume_comments:
            serialized_comments.append({'comment':comment.comment, 'id':comment.id, 'x':comment.x, 'y':comment.y})
        print serialized_comments
        print simplejson.dumps(serialized_comments)
        return render_to_response('individual_resume.html', {'resume':unique_resume, 'resume_comments':simplejson.dumps(serialized_comments), 'resume_exists':True}, RequestContext(request))
    except Exception as e:
        print e
        return render_to_response('individual_resume.html', {'resume_exists':False}, RequestContext(request))

def sign_s3_upload(request):
    AWS_ACCESS_KEY = 'AKIAJMUV3JF5IGAOPF3A'
    AWS_SECRET_KEY = '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'
    S3_BUCKET = 'resumefeed'

    digest = '+'
    json_results = ''

    while '+' in digest:
        lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(30)]
        object_name = request.GET['s3_object_name'] + "".join(lst) # creates a unique name 
        mime_type = request.GET['s3_object_type']

        expires = int(time.time()+3600)
        amz_headers = "x-amz-acl:public-read"

        put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

        digest = base64.encodestring(hmac.new(AWS_SECRET_KEY,put_request.encode('utf-8'), sha).digest())
        signature = urllib.quote_plus(digest.strip())

        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
        signed_request = '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature)

        json_results = simplejson.dumps({
            'signed_request': signed_request,
            'url': url
        })

    return HttpResponse(json_results, mimetype='application/json')

def submit_resume(request):
    resume_url = request.POST["resume_url"]
    return simplejson.dumps({'success': True})