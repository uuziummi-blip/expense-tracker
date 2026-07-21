from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    TYPE_CHOICES = (
        ("Income", "Income"),
        ("Expense", "Expense"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    color = models.CharField(max_length=7, default="#000000")  # Hex color code
    icon = models.CharField(max_length=50, blank=True, null=True)  # For UI icons
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"  # Fixes spelling in the Admin panel

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    PAYMENT_CHOICES = (
        ("Cash", "Cash"),
        ("Card", "Card"),
        ("Bank", "Bank"),
        ("JazzCash", "JazzCash"),
        ("EasyPaisa", "EasyPaisa"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default="Cash"
    )
    receipt = models.ImageField(upload_to="receipts/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - Rs {self.amount}"
