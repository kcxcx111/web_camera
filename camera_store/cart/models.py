from django.db import models
from store.models import Product
from django.contrib.auth.models import User

class SavedCart(models.Model):
    """Model to save a user's cart for later"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_carts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username} created at {self.created.strftime('%Y-%m-%d %H:%M')}"
    
class SavedCartItem(models.Model):
    """Items in a saved cart"""
    saved_cart = models.ForeignKey(SavedCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"