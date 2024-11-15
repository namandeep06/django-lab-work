# forms.py

from django import forms
from .models import OrderItem

# Form based on OrderItem model
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'client', 'quantity']  # Use 'quantity' instead of 'items_ordered'
        widgets = {
            'client': forms.RadioSelect
        }
        labels = {
            'quantity': 'Quantity',
            'client': 'Client Name'
        }

class InterestForm(forms.Form):
    interested = forms.ChoiceField(choices=[(1, "Yes"), (0, "No")], widget=forms.RadioSelect)
    quantity = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label='Additional Comments')
