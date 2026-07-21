from django.contrib import admin
from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # What columns show up in the list view
    list_display = ("name", "user", "type", "created_at")
    # Adds a filter sidebar
    list_filter = ("type", "user")
    # Adds a search bar
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "date", "payment_method")
    list_filter = ("date", "payment_method", "category__type")
    search_fields = ("description", "user__username", "category__name")
