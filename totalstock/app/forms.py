from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'weight', 'dimension_x', 'dimension_y', 'dimension_z', 'unit_of_measure']


class SearchItemForm(forms.Form):
    name = forms.CharField(required=False, label='Item Name')
    location = forms.CharField(required=False, label='Location')
    site = forms.CharField(required=False, label='Site')

    def search(self):
        # Retrieve cleaned data from the form
        name = self.cleaned_data.get('name')
        location = self.cleaned_data.get('location')
        site = self.cleaned_data.get('site')

        # Filter items based on provided parameters
        items = Item.objects.all()

        if name:
            items = items.filter(name__icontains=name)

        if location:
            items = items.filter(stock__location__name__icontains=location)

        if site:
            items = items.filter(stock__location__Site__name__icontains=site)

        return items
