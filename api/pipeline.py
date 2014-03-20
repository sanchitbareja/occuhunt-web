from django.contrib.auth.models import Group
from mailer import send_mail
from django.shortcuts import redirect
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
            if 'verified_email' in request.session.keys() and 'school_network' in request.session.keys() and 'email_identifier' in request.session.keys():
                print request.session['verified_email']
                print request.session['school_network']
                print request.session['email_identifier']
                user.student.verified_email = request.session['verified_email']+request.session['email_identifier']
                if request.session['school_network'] == 1:
                    print 9
                    g = Group.objects.get(name='UC Berkeley')
                    user.student.groups.add(g)
                if request.session['school_network'] == 2:
                    print 9
                    g = Group.objects.get(name='UC Berkeley ISchool')
                    user.student.groups.add(g)
                if request.session['school_network'] == 3:
                    print 9
                    g = Group.objects.get(name='San Jose State University School of Library and Information Science')
                    user.student.groups.add(g)
                if request.session['school_network'] == 4:
                    print 9
                    g = Group.objects.get(name='Academy of Art')
                    user.student.groups.add(g)
                user.student.save()
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
        if 'verified_email' in request.session.keys() and 'school_network' in request.session.keys() and 'email_identifier' in request.session.keys():
            # save network and verified email and convert to student
            print 8
            student_user = Student(user_ptr_id=user)
            student_user.__dict__.update(user.__dict__)
            student_user.verified_email = request.session['verified_email']+request.session['email_identifier']
            if request.session['school_network'] == 1:
                print 9
                g = Group.objects.get(name='UC Berkeley')
                student_user.groups.add(g)
            if request.session['school_network'] == 2:
                print 9
                g = Group.objects.get(name='UC Berkeley ISchool')
                student_user.groups.add(g)
            if request.session['school_network'] == 3:
                print 9
                g = Group.objects.get(name='San Jose State University School of Library and Information Science')
                student_user.groups.add(g)
            if request.session['school_network'] == 4:
                print 9
                g = Group.objects.get(name='Academy of Art')
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
            send_mail('[Occuhunt] Verify your network.', 'Click on the following link to verify your network: '+verification_url, from_email, [to_email], fail_silently=False)
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
        if type(kwargs['response']['educations']['education']) == type({}):
            if "University of California, Berkeley".lower() in kwargs['response']['educations']['education']['school-name'].lower():
                    g = Group.objects.get(name='UC Berkeley')
                    user = kwargs['user']
                    user.groups.add(g)
                    user.save()
            elif "University of California Berkeley".lower() in kwargs['response']['educations']['education']['school-name'].lower():
                    g = Group.objects.get(name='UC Berkeley')
                    user = kwargs['user']
                    user.groups.add(g)
                    user.save()
            elif "UC Berkeley".lower() in kwargs['response']['educations']['education']['school-name'].lower():
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
                elif "University of California Berkeley".lower() in kwargs['response']['educations']['education']['school-name'].lower():
                    g = Group.objects.get(name='UC Berkeley')
                    user = kwargs['user']
                    user.groups.add(g)
                    user.save()
                elif "UC Berkeley".lower() in kwargs['response']['educations']['education']['school-name'].lower():
                        g = Group.objects.get(name='UC Berkeley')
                        user = kwargs['user']
                        user.groups.add(g)
                        user.save()
    except Exception as e:
        print e