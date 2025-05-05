from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.search_products, name='search_products'),
    path('api/search/', views.search_products_api, name='search_products_api'),
    path('category/<slug:category_slug>/', views.product_list, name='category_list'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
