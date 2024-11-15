from django.db import models
from django.contrib.auth.models import User

# Model representing the type/category of items (e.g., fruits, vegetables)
class Type(models.Model):
    name = models.CharField(max_length=200)  # Name of the item type

    def __str__(self):
        return self.name  # Display name of the type in admin panel


# Model representing the grocery items
class Item(models.Model):
    type = models.ForeignKey(Type, related_name='items', on_delete=models.CASCADE)  # Foreign key to Type model
    name = models.CharField(max_length=200)  # Name of the item
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the item
    stock = models.PositiveIntegerField(default=100)  # Available stock of the item
    available = models.BooleanField(default=True)  # Item availability status
    description = models.TextField(null=True, blank=True)  # New optional description field
    interested = models.PositiveIntegerField(default=0)  # New field to track interest in the item

    def __str__(self):
        return f'{self.name} - {self.type}'

    # Optional method to add more meaningful info
    def is_available(self):
        return self.available

    # Method to replenish the stock for a particular item
    def topup(self):
        self.stock += 50
        self.save()  # Save the updated stock to the database


# Model representing the client, extending from Django's built-in User model
class Client(User):
    CITY_CHOICES = [
        ('WD', 'Windsor'),
        ('TO', 'Toronto'),
        ('CH', 'Chatham'),  # Changed the default city to Chatham
        ('WL', 'Waterloo'),
    ]
    shipping_address = models.CharField(max_length=300, null=True, blank=True)  # Shipping address of the client
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='CH')  # Client's city, with Chatham as default
    interested_in = models.ManyToManyField(Type)  # Types of items the client is interested in
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # New phone number field

    def __str__(self):
        return f'{self.username} ({self.city})'


# Model representing the orders placed by clients
class OrderItem(models.Model):
    STATUS_CHOICES = [
        (0, 'Cancelled'),  # Order cancelled
        (1, 'Placed'),     # Order placed
        (2, 'Shipped'),    # Order shipped
        (3, 'Delivered'),  # Order delivered
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # ForeignKey to the Item model (ordered item)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # ForeignKey to the Client model (client who ordered)
    quantity = models.PositiveIntegerField()  # Number of items ordered
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)  # Order status with choices (0,1,2,3)
    last_updated = models.DateTimeField(auto_now=True)  # Date when the order was last updated, auto-set on update

    def __str__(self):
        return f'Order by {self.client.username} for {self.item.name}'

    # Method to calculate the total price of the order
    def total_price(self):
        return self.quantity * self.item.price


class LabMember(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    personal_page = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
