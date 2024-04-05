from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
# Create your views here.
from .models import Item, List
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home_page(request):
    return render(request, "home.html")

from django.shortcuts import render
from django.http import JsonResponse
from .models import Item

def todo_page(request):
    return render(request, "todo.html")


def new_list(request):
    nulist = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=nulist)
    return redirect(f"http://127.0.0.1:8000/polls/todo/lists/{nulist.id}/")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    return render(request, "lists.html", {"list": our_list})

def add_item(request, list_id):
    our_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=our_list)
    return redirect(f"http://127.0.0.1:8000/polls/todo/lists/{our_list.id}/")

def get_users(request):
    return render(request, "users.html")


def user_details(request, user_id):
    with open('/Users/sumitkam/TDD_Tutorial/polls/sample.json') as f:
        data = json.load(f)

        users = data['users']
    for user in users:
        if user['id'] == user_id:
            return render(request, 'user.html', {'user': user})

