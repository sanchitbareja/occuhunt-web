from django.contrib.auth.models import Group

def linkedin_test(request, backend, *args, **kwargs):
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