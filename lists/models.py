from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

MAX_NAME_LEN = 200
MAX_NOTES_LEN = 500
MAX_LINK_LEN = 600

class WishList(models.Model): 
    name = models.CharField(max_length=MAX_NAME_LEN)
    owner = models.ForeignKey(User)
    private = models.BooleanField(default=False)
    description = models.CharField(max_length=MAX_NOTES_LEN)
    
class Product(models.Model): 
    name = models.CharField(max_length=MAX_NAME_LEN)
    notes = models.CharField(max_length=MAX_NOTES_LEN)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.CharField(max_length=MAX_LINK_LEN)
    thumbnail = models.CharField(max_length=MAX_LINK_LEN)
    
    wishlist = models.ForeignKey(WishList)
