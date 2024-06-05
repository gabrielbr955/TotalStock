from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import ItemForm, SearchItemForm, IssuanceForm, ReceivingForm, AdjustStockForm
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import User, Site, Location, Item, Stock


def is_manager(user):
    return user.is_authenticated and user.is_manager
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


def issuance(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)  # Get Stock object by ID
    item = stock.item  # Get related Item object
    site = stock.location.Site  # Get Site related to the Stock's location

    message =""

    if request.method == 'POST':
        form = IssuanceForm(request.POST)
        if form.is_valid():
            units_used = form.cleaned_data['units_used']
            if units_used > 0 and units_used <= stock.quantity:
                stock.quantity -= units_used  # Decrease stock amount
                stock.save()                
                message = "Stock quantity updated."
            else:
                message = "Error: Invalid number of units. Please enter a valid quantity."
    else:
        form = IssuanceForm()

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
    return render(request, 'issuance.html', context)

@user_passes_test(is_manager)
def receiving(request):
    if request.method == 'POST':
        form = ReceivingForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            site = form.cleaned_data['site']
            quantity = form.cleaned_data['quantity']
            
            # Check if the item is already in stock at any location for the selected site
            existing_stocks = Stock.objects.filter(item=item, site=site)

            context = {
                'item': item,
                'site': site,
                'quantity': quantity,
                'existing_stocks': existing_stocks,
            }
            return render(request, 'receiving_confirmation.html', context)
    else:
        form = ReceivingForm()

    context = {
        'form': form,
    }
    return render(request, 'receiving.html', context)


"""
def adjust_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        form = AdjustStockForm(request.POST)
        if form.is_valid():
            # Update stock manually
            stock.quantity = form.cleaned_data['quantity']
            stock.save()
            return redirect('some_view_name')  # Redirect to an appropriate view after adjusting stock
    else:
        form = AdjustStockForm(initial={'quantity': stock.quantity})  # Populate form with initial quantity
    context = {
        'form': form,
        'stock': stock,
    }
    return render(request, 'adjust_stock.html', context)
"""


@user_passes_test(is_manager)
def adjust_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)  # Get Stock object by ID
    item = stock.item  # Get related Item object
    site = stock.location.Site  # Get Site related to the Stock's location

    message =""

    initial_data = {
        'quantity': stock.quantity,
        'site': site,
        'location': stock.location,
    }

    if request.method == 'POST':
        form = AdjustStockForm(request.POST, initial=initial_data)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            new_site = form.cleaned_data['site']
            new_location = form.cleaned_data['location']

            if quantity >= 0:
                stock.quantity = quantity
                stock.location = new_location
                stock.location.Site = new_site
                stock.save()
                message = "Stock updated."
            else:
                message = "Error: Invalid number of units. Please enter a valid quantity."
    else:
        form = AdjustStockForm(initial= initial_data )


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
    return render(request, 'adjust_stock.html', context)

@user_passes_test(is_manager)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})