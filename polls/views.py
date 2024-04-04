from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
# Create your views here.
from .models import Item
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home_page(request):
    return render(request, "home.html")

from django.shortcuts import render
from django.http import JsonResponse
from .models import Item

def todo_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("http://127.0.0.1:8000/polls/todo/")

    items = Item.objects.all()
    return render(request, "todo.html", {"items": items})



def get_users(request):
    return render(request, "users.html")


def user_details(request, user_id):
    with open('/Users/sumitkam/TDD_Tutorial/polls/sample.json') as f:
        data = json.load(f)

        users = data['users']
    for user in users:
        if user['id'] == user_id:
            return render(request, 'user.html', {'user': user})

