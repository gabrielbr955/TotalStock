from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .forms import ItemForm, SearchItemForm, IssuanceForm, AdjustStockForm, EntryStockForm, CreateStockForm
from .models import User, Stock, Item, Site, Location


def is_manager(user):
    return (user.is_authenticated
            and user.groups.filter(name='manager').exists())


def is_staff(user):
    return (user.is_authenticated
            and (user.groups.filter(name='staff').exists()
                 or user.groups.filter(name='manager').exists()))


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


@user_passes_test(is_staff)
def entry_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)  # Get Stock object by ID
    item = stock.item  # Get related Item object
    site = stock.location.Site  # Get Site related to the Stock's location

    message = ""

    if request.method == 'POST':
        form = EntryStockForm(request.POST)
        if form.is_valid():
            units_received = form.cleaned_data['units_received']
            if units_received > 0:
                stock.quantity += units_received  # Decrease stock amount
                stock.save()
                message = "Stock quantity updated."
            else:
                message = "Error: Invalid number of units. Please enter a valid quantity."
    else:
        form = EntryStockForm()

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
    return render(request, 'entry_stock.html', context)


@user_passes_test(is_staff)
def create_stock(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    message = ""

    if request.method == 'POST':
        form = CreateStockForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            site = form.cleaned_data['site']
            location = form.cleaned_data['location']

            if quantity <= 0:
                message = "Error: Invalid number of units. Please enter a valid quantity."
            elif (location and not site) or (not location and site):
                message = "Error: Invalid Location and Site combination"
            elif not location or not site:
                message = "Error: invalid Location and Site combination"
            else:
                if location in site.locations.all():
                    stock = Stock(item=item, location=location, site=site, quantity=quantity)
                    stock.save()
                    message = "Stock creation Successful"
                else:
                    message = "Error: invalid Location and Site combination"
    else:
        form = CreateStockForm()

    context = {
        'item_id': item.id,
        'item_name': item.name,
        'item_description': item.description,
        'form': form,
        'message': message,
    }
    return render(request, 'create_stock.html', context)


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

            if new_quantity <= 0:
                message = "Error: Invalid number of units. Please enter a valid quantity."
            elif (new_location and not new_site) or (not new_location and new_site):
                message = "Error: invalid Location and Site combination"
            elif not new_location and not new_site:
                stock.quantity = new_quantity
                stock.save()
                message = "Adjust successful"
            else:
                if new_location in new_site.locations.all():
                    stock.quantity = new_quantity
                    stock.location = new_location
                    stock.location.Site = new_site
                    stock.save()
                    message = "Adjust successful"
                else:
                    message = "Error: invalid Location and Site combination"
    else:
        # Initialize the form with the current stock details
        form = AdjustStockForm(initial={'quantity': stock.quantity, 'site': site, 'location': stock.location})

    context = {
        'stock_id': stock_id,
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
def delete_stock(request, stock_id):
    if request.method == 'POST':
        stock = get_object_or_404(Stock, id=stock_id)
        stock.delete()
        return redirect('search_item')  # Redirect to the search page or any other appropriate page

    return HttpResponseForbidden("You are not allowed to access this page.")

@user_passes_test(is_manager)
def manage_users(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        is_manager = request.POST.get('is_manager') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'

        user = User.objects.get(id=user_id)

        manager_group = Group.objects.get(name='manager')
        staff_group = Group.objects.get(name='staff')

        if is_manager:
            user.groups.add(manager_group)
        else:
            user.groups.remove(manager_group)

        if is_staff:
            user.groups.add(staff_group)
        else:
            user.groups.remove(staff_group)

        user.save()

        return redirect('manage_users')

    users = User.objects.all()
    users = User.objects.all()
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_manager': user.groups.filter(name='manager').exists(),
            'is_staff': user.groups.filter(name='staff').exists(),
        })

    return render(request, 'manage_users.html', {'users': user_data})
