from django import forms
from .models import Item, Stock


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'weight', 'dimension_x', 'dimension_y', 'dimension_z', 'unit_of_measure']


class SearchItemForm(forms.Form):
    name = forms.CharField(required=False, label='Item Name')
    description = forms.CharField(required=False, label='Description')
    location = forms.CharField(required=False, label='Location')
    site = forms.CharField(required=False, label='Site')

    def search(self):
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

class ConsumptionForm(forms.Form):
    units_used = forms.IntegerField(label='Units Used', min_value=1)