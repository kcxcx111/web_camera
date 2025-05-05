from django.contrib import admin
from .models import SavedCart, SavedCartItem

class SavedCartItemInline(admin.TabularInline):
    model = SavedCartItem
    raw_id_fields = ['product']
    extra = 1

@admin.register(SavedCart)
class SavedCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [SavedCartItemInline]