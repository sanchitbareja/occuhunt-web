from django.contrib.auth.models import Group

def linkedin_test(request, backend, details, response, social_user, uid, user, *args, **kwargs):
    try:
        for education in response['educations']['education']:
            if education['school-name'] == "University of California, Berkeley":
                g = Group.objects.get(name='UC Berkeley')
                user.groups.add(g)
                user.save()
    except Exception as e:
        print e