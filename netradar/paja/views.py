from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Template
# Create your views here.
def home(request):
    return render(request, "base.html")

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register_view(request):
    if request.method=='POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('login')

def pong(request):
    return render(request, "pong.html")
