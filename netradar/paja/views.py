from django.shortcuts import render
from django.http import HttpResponse

from django.template import Template
# Create your views here.
def home(request):
    return render(request, "base.html")

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def pong(request):
    return render(request, "pong.html")
