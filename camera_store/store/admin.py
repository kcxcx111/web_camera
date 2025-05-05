from django.contrib import admin
from .models import Category, Product, ProductImage, Specification

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated', 'featured']
    list_filter = ['available', 'created', 'updated', 'featured', 'category']
    list_editable = ['price', 'stock', 'available', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, SpecificationInline]
    search_fields = ['name', 'description']