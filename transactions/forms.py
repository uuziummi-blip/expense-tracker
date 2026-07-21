from django import forms
from .models import Category, Transaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # We purposely leave out 'user' because we will set it automatically in the background
        fields = ["name", "type", "color", "icon"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "category",
            "amount",
            "description",
            "date",
            "payment_method",
            "receipt",
        ]
        # This makes the date field show a nice calendar picker in the browser
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

    # CRITICAL SECURITY STEP: We must filter the category dropdown so User A doesn't see User B's categories
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user)
