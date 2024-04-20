from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import ItemForm, SearchItemForm

from .models import User, Site, Location, Item, Stock


# Create your views here.
def main_page(request):
    if request.user.is_authenticated:
        return render(request, 'app.html')
    else:
        return redirect('app_login')


def app_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
    return render(request, 'login.html')


def app_logout(request):
    logout(request)
    return redirect('app_login')


def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_page')  # Redirect to main page after item creation
    else:
        form = ItemForm()

    return render(request, 'create_item.html', {'form': form})


def search_item(request):
    form = SearchItemForm(request.GET)

    if form.is_valid():
        items = form.search()
    else:
        items = None

    return render(request, 'search_item.html', {'form': form, 'items': items})

"""

def add_item(request, list_id):
    item_title = request.POST.get('item_title')
    list = get_object_or_404(List, pk=list_id, user=request.user)
    item = Item(title=item_title, list=list)
    item.save()
    return redirect('todo_list', list_id=list_id)

"""