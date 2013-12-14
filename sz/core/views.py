from django.http import HttpResponse
from django.shortcuts import redirect

from .models import RegistrationProfile
from lebowski.api.views.users import UsersCreate as lebowski_create_user


def index(request):
    return redirect('/!/index.html')
    # return redirect('/tmpviews/index.html')

def activate(request, activation_key):
	user = RegistrationProfile.objects.activate(activation_key)
	if user:
		r = lebowski_create_user().create({u'email': user.email}) 		
		return HttpResponse("Yosick is happy. You are awesome ^___^. %s"%r.get('data',''))
	else:
		return HttpResponse("Yosick is upset. Bad key :(")
