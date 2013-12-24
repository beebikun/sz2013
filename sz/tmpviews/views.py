# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response

from django.template import Context, loader


context = Context({})
def index(request):
    template = loader.get_template('tmp_views/index.html')    
    return HttpResponse(template.render({}))

def user_registration(request):
    template = loader.get_template('tmp_views/user-registration.html')
    return HttpResponse(template.render(context))