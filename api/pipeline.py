from django.contrib.auth.models import Group
from django.shortcuts import redirect
from users.models import User, Student
from social.pipeline.partial import partial
import oauth2 as oauth
import time, json

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
                user.student.save()
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
            student_user.save()
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