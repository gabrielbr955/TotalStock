from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import ItemForm, SearchItemForm, ConsumptionForm

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


def consumption_view(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)  # Get Stock object by ID
    item = stock.item  # Get related Item object
    site = stock.location.Site  # Get Site related to the Stock's location

    message =""

    if request.method == 'POST':
        form = ConsumptionForm(request.POST)
        if form.is_valid():
            units_used = form.cleaned_data['units_used']
            if units_used > 0 and units_used <= stock.quantity:
                stock.quantity -= units_used  # Decrease stock amount
                stock.save()                
                message = "Stock quantity updated."
            else:
                message = "Error: Invalid number of units. Please enter a valid quantity."
    else:
        form = ConsumptionForm()

    context = {
        'item_id': item.id,
        'item_name': item.name,
        'item_description': item.description,
        'location': stock.location.name,
        'site_name': site.name,
        'stock_quantity': stock.quantity,
        'form': form,
        'message': message,
    }
    return render(request, 'consumption.html', context)