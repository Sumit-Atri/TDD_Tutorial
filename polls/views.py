from django.http import HttpResponse
from django.shortcuts import render
import json
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home_page(request):
    return render(request, "home.html")

def get_users(request):
    return render(request, "users.html")


def user_details(request, user_id):
    with open('/Users/sumitkam/TDD_Tutorial/polls/sample.json') as f:
        data = json.load(f)

        users = data['users']
    for user in users:
        if user['id'] == user_id:
            return render(request, 'user.html', {'user': user})

