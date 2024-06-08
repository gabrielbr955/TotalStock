from django import forms
from .models import Item, Stock, Site, Location


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'weight', 'unit_of_measure']


class SearchItemForm(forms.Form):
    name = forms.CharField(required=False, label='Item Name')
    description = forms.CharField(required=False, label='Description')
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label='Location')
    site = forms.ModelChoiceField(queryset=Site.objects.all(), required=False, label='Site')

    #    location = forms.CharField(required=False, label='Location')
    #    site = forms.CharField(required=False, label='Site')

    def search_stock(self):
        # Retrieve cleaned data from the form
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        location = self.cleaned_data.get('location')
        site = self.cleaned_data.get('site')

        # Filter items based on provided parameters
        stocks = Stock.objects.all()

        if name:
            stocks = stocks.filter(item__name__icontains=name)

        if description:
            stocks = stocks.filter(item__description__icontains=description)

        if location:
            stocks = stocks.filter(location__name__icontains=location)

        if site:
            stocks = stocks.filter(location__Site__name__icontains=site)

        # Return the list of filtered stocks
        return stocks

    def search_remaining_items(self):
        # Retrieve cleaned data from the form
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        location = self.cleaned_data.get('location')
        site = self.cleaned_data.get('site')

        # Filter items based on provided parameters
        remaining_items = Item.objects.exclude(stock__isnull=False)

        if name:
            remaining_items = remaining_items.filter(name__icontains=name)

        if description:
            remaining_items = remaining_items.filter(description__icontains=description)

        if site:
            remaining_items = remaining_items.filter(stock__location__Site=site)

        if location:
            remaining_items = remaining_items.filter(stock__location=location)

        return remaining_items


class IssuanceForm(forms.Form):
    units_used = forms.IntegerField(label='Units Used', min_value=1)


class AdjustStockForm(forms.Form):
    quantity = forms.DecimalField(max_digits=10, decimal_places=0, min_value=0, label='New Quantity', initial=0)
    site = forms.ModelChoiceField(queryset=Site.objects.all(), label='New site', required=False)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label='New location', required=False)


class EntryStockForm(forms.Form):
    units_received = forms.DecimalField(max_digits=10, decimal_places=0, min_value=0, label='Quantity', initial=0)
