from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Template
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.base import View
from social_auth.backends.exceptions import AuthFailed
from social_auth.views import complete
# Create your views here.
def home(request):
    return render(request, "base.html")

def register_view(request):
    return render(request, "base.html")
    # if request.method=='POST':
    #     form = MyUserCreationForm(request.POST)
    #     if form.is_valid():
    #         return HttpResponseRedirect('login')

def mydata_view(request):
    return render(request, "data.html")
def pong(request):
    return render(request, "pong.html")

def login(request):
    return render(request, "login.html")

class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        try:
            return complete(request, backend, *args, **kwargs)
        except AuthFailed:
            messages.error(request, "Your Google Apps domain isn't authorized for this app")
            return HttpResponseRedirect(reverse('login'))


class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)
