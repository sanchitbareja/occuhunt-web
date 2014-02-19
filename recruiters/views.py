from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
import os, time, simplejson, base64, urllib, hmac, sha, random, string
from string import strip
from django.http import Http404
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Avg, Count

from occuhunt.settings import EMAIL_MASTERS
from companies.models import Company
from jobs.models import Job
from users.models import User
from resumes.models import Resume
from applications.models import Application
from fairs.models import Fair

from social_auth import __version__ as version
from social_auth.utils import setting

def recruiter_splash(request):
    return render_to_response('recruiter/recruiter_splash.html', {'version': version}, RequestContext(request))

def recruiter_login(request):
    print request.POST
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return redirect('/recruiter/hire/')
        else:
            # Return a 'disabled account' error message
            return render_to_response('recruiter/recruiter_splash.html', {'version': version, 'error_loggin_in':True}, RequestContext(request))
    else:
        # Return an 'invalid login' error message.
        return render_to_response('recruiter/recruiter_splash.html', {'version': version, 'error_loggin_in':True}, RequestContext(request))

@csrf_exempt
def recruiter_login_third_party(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    results = {'success':False}
    if user is not None:
        if user.is_active:
            if user.recruiter_for:
                results['success'] = True
                results['company_id'] = user.recruiter_for.id
                json_results = simplejson.dumps(results)
                return HttpResponse(json_results, mimetype='application/json')
    # Return an 'invalid login' error message.
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')

def check_if_recruiter(user):
    if user.recruiter_for:
        return True
    else:
        return False

@login_required
@user_passes_test(check_if_recruiter, redirect_field_name='')
def recruiter_hire(request):
    """Recruiter interface for hiring candidates"""
    recruiter_id = request.user.recruiter_for.id
    return render_to_response('recruiter/recruiter_hire.html', {'version': version, 'recruiter_id':recruiter_id}, RequestContext(request))

@login_required
@user_passes_test(check_if_recruiter, redirect_field_name='')
def recruiter_analytics(request):
    """Recruiter interface for hiring candidates"""
    # if POST, return json formatted data according to query
        # check for existence of company_id and fair_id
        # try getting the following data:
            # 1. # of students that attended the fair
            # 2. # of students that applied to them spcifically
            # 3. # of students that they are calling for interview
            # 4. # of students they rejected
            # 5. avg number of applications received by other companies
    # else, return analytics page
    if request.method == 'POST':
        results = {'success':False}
        if 'company_id' in request.POST.keys() and 'fair_id' in request.POST.keys():
            try:
                company_id = request.POST['company_id']
                fair_id = request.POST['fair_id']
                company = Company.objects.get(id=company_id)
                fair = Fair.objects.get(id=fair_id)
                num_attendees = Application.objects.filter(fair=fair).distinct('user').count()
                num_applicants = Application.objects.filter(fair=fair, company=company).count()
                num_applicants_to_interview = Application.objects.filter(fair=fair, company=company, status=4).count()
                num_applicants_rejected = Application.objects.filter(fair=fair, company=company, status=3).count()
                # 1. companies that attended the fair
                # 2. annontate each company with the number of applications they get
                # 3. annotate each company with application count
                # 4. get average of the application count
                avg_num_applications = Company.objects.filter(id__in=Application.objects.filter(fair=fair).distinct('company').values_list('company__id')).annotate(application_count=Count('application')).aggregate(avg_applications_per_company=Avg('application_count'))
                results['success'] = True
                results['num_attendees'] = num_attendees
                results['num_applicants'] = num_applicants
                results['num_applicants_to_interview'] = num_applicants_to_interview
                results['num_applicants_rejected'] = num_applicants_rejected
                results['avg_num_applications'] = avg_num_applications['avg_applications_per_company']
            except:
                results['success'] = False
        json_results = simplejson.dumps(results)
        return HttpResponse(json_results, mimetype='application/json')
    else:
        recruiter_id = request.user.recruiter_for.id
        return render_to_response('recruiter/recruiter_analytics.html', {'version': version, 'recruiter_id':recruiter_id}, RequestContext(request))

@login_required
@user_passes_test(check_if_recruiter, redirect_field_name='')
def recruiter_market(request):
    """Recruiter interface for editting their profile"""
    company = Company.objects.get(id=305)
    jobs = Job.objects.filter(company=company, deactivate=False)
    recruiter_id = request.user.recruiter_for.id
    return render_to_response('recruiter/recruiter_market.html', {'version': version, 'company':company, 'jobs':jobs, 'recruiter_id':recruiter_id}, RequestContext(request))

@login_required
@user_passes_test(check_if_recruiter, redirect_field_name='')
def recruiter_sell(request):
    """Recruiter interface for sponsoring events"""
    recruiter_id = request.user.recruiter_for.id
    return render_to_response('recruiter/recruiter_sell.html', {'version': version, 'recruiter_id':recruiter_id}, RequestContext(request))

def recruiter_sponsorship_request(request):
    """post sponsorship request form and send email"""
    results = {'success':False}
    if(request.method == u'POST'):
        POST = request.POST
        send_mail('[Occuhunt] Recruiter Sponsorship Request!', POST['sponsorRequest']+" Recruiter ID: "+POST['sponsorId']+" Event ID: "+POST['eventId'], 'occuhunt@gmail.com', EMAIL_MASTERS, fail_silently=False)
        results['success'] = True
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')

def download_pdf(request):
    """
    request download of PDF file

    - notify student of download
    """
    results = {'success':False}
    if(request.method == u'POST'):
        try:
            POST = request.POST
            application = Application.objects.get(id=POST['application_id'])
            user = User.objects.get(id=application.user.id)
            resume = Resume.objects.filter(user=user, showcase=True, original=True).order_by('-timestamp')
            if len(resume) > 0:
                resume = resume[0]
                results['resume_pdf'] = resume.url
                results['success'] = True
            else:
                # send student notification to upload pdf again.
                results['success'] = False
        except:
            pass
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')
    