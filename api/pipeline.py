from django.contrib.auth.models import Group
from mailer import send_mail
from django.template import Context, RequestContext
from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse
from users.models import User, Student
from social.pipeline.partial import partial
from occuhunt.settings import BASE_URL
import oauth2 as oauth
import time, json, hashlib, datetime
import os

@partial
def create_password(request, backend, *args, **kwargs):
    """
    1. existing student
        1. verified -> good to go
        2. not verified but we have email (i.e. hasn't clicked on link in email) -> resend verification email
        3. not verified and no email -> redirect
    2. new student
        1. if coming back from partial -> create student record and update, send verification email
        2. first entry -> redirect
    """
    print 1
    user = kwargs['user']
    if hasattr(user, 'student'):
        print 2
        print user.student.verified_email
        if user.student.verified_email:
            print 3
            if user.is_verified:
                print 4
                # everything's good!
                pass
            else:
                print 5
                # reminder message to update link
                pass
        else:
            print 6
            if 'verified_email' in request.session.keys() and 'school_network' in request.session.keys():
                print request.session['verified_email']
                print request.session['school_network']
                user.student.verified_email = request.session['verified_email']
                user.student.save()
                
                g = Group.objects.get(id=request.session['school_network'])
                user.groups.add(g)
                user.save()

                # send user verification email
                from_email = 'occuhunt@gmail.com'
                to_email = user.student.verified_email
                verification_token = hashlib.sha224(user.first_name+user.last_name+user.student.verified_email+request.session['school_network']+str(datetime.datetime.now())).hexdigest()
                verification_url = BASE_URL+"verify/"+verification_token+"/"
                user.verification_token = verification_token
                user.is_verified = False
                user.save()
                send_mail('[Occuhunt] Verify your network.', 'Click on the following link to verify your network: '+verification_url, from_email, [to_email], fail_silently=False)
                os.system('python manage.py send_mail')
            else:
                return redirect('get-email-network')
    else:
        print 7
        if 'verified_email' in request.session.keys() and 'school_network' in request.session.keys():
            # save network and verified email and convert to student
            print 8
            student_user = Student(user_ptr_id=user.id)
            student_user.__dict__.update(user.__dict__)
            student_user.verified_email = request.session['verified_email']

            g = Group.objects.get(id=request.session['school_network'])
            student_user.groups.add(g)
            student_user.save()

            # send student verification email
            from_email = 'occuhunt@gmail.com'
            to_email = student_user.verified_email
            verification_token = hashlib.sha224(student_user.first_name+student_user.last_name+student_user.verified_email+request.session['school_network']+str(datetime.datetime.now())).hexdigest()
            verification_url = BASE_URL+"verify/"+verification_token+"/"
            user.verification_token = verification_token
            user.is_verified = False
            user.save()
            # send_mail('[Occuhunt] Verify your network.', 'Click on the following link to verify your network: '+verification_url, from_email, [to_email], fail_silently=False)
            os.system('python manage.py send_mail')
            print "sent email"
        else:
            print 10
            # create user and password for student
            uid = kwargs['uid']
            user.linkedin_uid = uid
            user.set_password(uid)
            user.save()
            # redirect to confirm network
            return redirect('get-email-network')

def associate_group(request, backend, *args, **kwargs):
    """
    1. Save the user as a student
    2. Associate the student with his network but leave him as unverified
    3. Send him verification email
        3.1 encode a token that contains network, email, user_id
        3.2 create a link that the user can click on to verify email - needs to include token
        3.3 send email with link
    """
    try:
        print kwargs
    except Exception as e:
        print e