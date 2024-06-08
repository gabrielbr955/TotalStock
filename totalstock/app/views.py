from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ItemForm, SearchItemForm, IssuanceForm, AdjustStockForm
from .models import User, Stock, Item, Site, Location


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


def search_item(request):
    form = SearchItemForm(request.GET)

    if form.is_valid():
        items = form.search_stock()
        remaining_items = form.search_remaining_items()
    else:
        items = None
        remaining_items = None

    return render(request, 'search_item.html', {'form': form, 'items': items, 'remaining_items': remaining_items})


def issuance(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)  # Get Stock object by ID
    item = stock.item  # Get related Item object
    site = stock.location.Site  # Get Site related to the Stock's location

    message = ""

    if request.method == 'POST':
        form = IssuanceForm(request.POST)
        if form.is_valid():
            units_used = form.cleaned_data['units_used']
            if 0 < units_used <= stock.quantity:
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
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_page')  # Redirect to main page after item creation
    else:
        form = ItemForm()

    return render(request, 'create_item.html', {'form': form})


@user_passes_test(is_manager)
def adjust_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)  # Get Stock object by ID
    item = stock.item  # Get related Item object
    site = stock.location.Site  # Get Site related to the Stock's location

    message = ""

    if request.method == 'POST':
        form = AdjustStockForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            new_site = form.cleaned_data['site']
            new_location = form.cleaned_data['location']

            if new_quantity >= 0:
                stock.quantity = new_quantity
                if new_location:
                    stock.location = new_location
                if new_site and stock.location.Site != new_site:
                    stock.location.Site = new_site
                stock.save()
                message = "Stock updated."
            else:
                message = "Error: Invalid number of units. Please enter a valid quantity."
    else:
        # Initialize the form with the current stock details
        form = AdjustStockForm(initial={'quantity': stock.quantity, 'site': site, 'location': stock.location})

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
