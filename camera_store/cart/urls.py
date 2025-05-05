from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('save/', views.save_cart_for_later, name='save_cart'),
    path('saved/', views.view_saved_carts, name='view_saved_carts'),
    path('load/<int:cart_id>/', views.load_saved_cart, name='load_saved_cart'),
    path('delete/<int:cart_id>/', views.delete_saved_cart, name='delete_saved_cart'),
]