from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home_page(request):
    return HttpResponse("<html><title>Polls</title></html>")