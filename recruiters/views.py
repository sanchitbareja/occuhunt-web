from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.servers.basehttp import FileWrapper
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
import os, time, simplejson, base64, urllib, hmac, sha, random, string
from string import strip
from django.http import Http404
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Avg, Count
import xlsxwriter

from occuhunt.settings import EMAIL_MASTERS
from companies.models import Company
from jobs.models import Job
from users.models import User
from resumes.models import Resume
from applications.models import Application
from fairs.models import Fair
from notifications.models import Notification

def recruiter_splash(request):
    return render_to_response('recruiter/recruiter_splash.html', {}, RequestContext(request))

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
            return render_to_response('recruiter/recruiter_splash.html', {'error_loggin_in':True}, RequestContext(request))
    else:
        # Return an 'invalid login' error message.
        return render_to_response('recruiter/recruiter_splash.html', {'error_loggin_in':True}, RequestContext(request))

@csrf_exempt
def recruiter_login_third_party(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    results = {'success':False}
    if user is not None:
        if user.is_active:
            if user.recruiter.company:
                results['success'] = True
                results['company_id'] = user.recruiter.company.id
                json_results = simplejson.dumps(results)
                return HttpResponse(json_results, mimetype='application/json')
    # Return an 'invalid login' error message.
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')

def check_if_recruiter(user):
    if user.recruiter.company:
        return True
    else:
        return False

@login_required
@user_passes_test(check_if_recruiter, redirect_field_name='')
def recruiter_hire(request):
    """Recruiter interface for hiring candidates"""
    recruiter_id = request.user.recruiter.company.id
    return render_to_response('recruiter/recruiter_hirev2.html', {'recruiter_id':recruiter_id}, RequestContext(request))

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
        recruiter_id = request.user.recruiter.company.id
        return render_to_response('recruiter/recruiter_analytics.html', {'recruiter_id':recruiter_id}, RequestContext(request))

@login_required
@user_passes_test(check_if_recruiter, redirect_field_name='')
def recruiter_market(request):
    """Recruiter interface for editting their profile"""
    company = Company.objects.get(id=request.user.recruiter.company.id)
    jobs = Job.objects.filter(company=company, deactivate=False)
    recruiter_id = request.user.recruiter.company.id
    return render_to_response('recruiter/recruiter_market.html', {'company':company, 'jobs':jobs, 'recruiter_id':recruiter_id}, RequestContext(request))

@login_required
@user_passes_test(check_if_recruiter, redirect_field_name='')
def recruiter_sell(request):
    """Recruiter interface for sponsoring events"""
    recruiter_id = request.user.recruiter.company.id
    return render_to_response('recruiter/recruiter_sell.html', {'recruiter_id':recruiter_id}, RequestContext(request))

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
                # notify user that application has been downloaded by company
                try:
                    new_notification = Notification(user=application.user, company=application.company, receiver=1, notification=2)
                    new_notification.save()
                except Exception, e:
                    print e
                    raise e
            else:
                # send student notification to upload pdf again.
                results['success'] = False
        except:
            pass
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')
    
def download_excel_to_export(request):
    """
    request download to export
    1. check if recruiter has replied to all the applicants from a fair
    2. If he has, then commence creation of excel sheet
    3. send excel file in response
    """
    if(request.method == u'POST'):
        POST = request.POST
        try:
            # get fair_id
            # get company_id
            fair = Fair.objects.get(id=POST['fair_id'])
            company = Company.objects.get(id=POST['company_id'])
            applications = Application.objects.filter(fair=fair, company=company)

            # the recruiter needs to accept or reject all the applications before he can download it
            if applications.filter(status=1).count() > 0:
                return HttpResponseNotFound("<h1>Sorry! You need to respond to all applicants before you can download the data. 'Interview' or 'Reject' all applicants at the fair. Thanks!</h1>")
            if applications.filter(status=2).count() > 0:
                return HttpResponseNotFound("<h1>Sorry! You need to respond to all applicants before you can download the data. 'Interview' or 'Reject' all applicants at the fair. Thanks!</h1>")
            # Create a workbook and add a worksheet.
            workbook = xlsxwriter.Workbook(''+fair.name+'_'+company.name+'.xlsx')
            worksheet = workbook.add_worksheet()

            # Write the titles of the cell in row 0
            worksheet.write(0, 0, 'First Name')
            worksheet.write(0, 1, 'Last Name')
            worksheet.write(0, 2, 'Email')
            worksheet.write(0, 3, 'Resume URL')
            worksheet.write(0, 4, 'Application Status')

            # Start from the first cell. Rows and columns are zero indexed. Start with row=1 as first row is for titles
            row = 1
            col = 0

            # Iterate over the data and write it out row by row.
            applications_enumerated = [(application.user.first_name, application.user.last_name, application.user.email, application.get_resume(), application.status) for application in applications]
            for first_name, last_name, email, resume_url, status in applications_enumerated:
                worksheet.write(row, col, first_name)
                worksheet.write(row, col + 1, last_name)
                worksheet.write(row, col + 2, email)
                worksheet.write(row, col + 3, resume_url)
                if status == 3:
                    worksheet.write(row, col + 4, "Rejected")
                if status == 4:
                    worksheet.write(row, col + 4, "To Interview")
                row += 1

            workbook.close()
            wrapper = FileWrapper(file(''+fair.name+'_'+company.name+'.xlsx'))
            response = HttpResponse(wrapper, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="'+fair.name+'_'+company.name+'.xlsx"'
            return response
        except Exception, e:
            # this is an error
            print e
            return HttpResponseNotFound("<h1>Oops! Our minions have failed us! Please try again later while our minions fix this.</h1>")
    else:
        # this is a get request
        # a get request should not be made at this point
        return HttpResponseNotFound("<h1>Sorry! This is an illegal request. Our minions do not recognize this command.</h1>")
