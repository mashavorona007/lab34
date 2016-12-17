from __future__ import unicode_literals

from decimal import Decimal

from django import forms

from lists.models import Product, MAX_NAME_LEN
from utils.decorators import html5_required


def get_field(Model, fieldName):
    return Model._meta.get_field(fieldName)
    
    
@html5_required
class ProductForm(forms.Form):
    item_name = forms.CharField(max_length=MAX_NAME_LEN)
    item_link = forms.URLField()
    
    item_price = forms.DecimalField(
        min_value=Decimal('0.00'),
        max_digits=get_field(Product, 'price').max_digits,
        decimal_places=get_field(Product, 'price').decimal_places,
    )
    
    item_description = forms.CharField(required=False)
    
    item_thumbnail = forms.URLField()
    
    