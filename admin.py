from django.contrib import admin
from .models import Type, Item, Client, OrderItem

# Register the Type model with the admin site
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the 'name' field in the admin list view

# Register the Item model with the admin site
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'stock', 'available')  # Fields to display in the admin list view
    list_filter = ('type', 'available')  # Add filters for type and availability
    search_fields = ('name',)  # Enable search by item name

# Register the Client model with the admin site
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'city', 'phone_number')  # Fields to display in the admin list view
    list_filter = ('city',)  # Filter clients by city
    search_fields = ('username', 'email')  # Enable search by username and email

# Register the OrderItem model with the admin site
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('client', 'item', 'quantity', 'status', 'last_updated')  # Fields to display in the admin list view
    list_filter = ('status', 'client')  # Filter orders by status and client
    search_fields = ('client__username', 'item__name')  # Enable search by client username and item name
from django.contrib import admin

# Register your models here.
