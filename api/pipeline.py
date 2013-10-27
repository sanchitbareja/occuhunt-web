from django.contrib.auth.models import Group

def linkedin_test(request, backend, *args, **kwargs):
    try:
        for education in kwargs['response']['educations']['education']:
            if education['school-name'] == "University of California, Berkeley":
                g = Group.objects.get(name='UC Berkeley')
                user = kwargs['user']
                user.groups.add(g)
                user.save()
    except Exception as e:
        print e