from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add-category/", views.add_category, name="add_category"),
    path("add-transaction/", views.add_transaction, name="add_transaction"),
    path("transactions/", views.transaction_list, name="transaction_list"),
    # Fixed paths below:
    path("transaction/<int:pk>/edit/", views.edit_transaction, name="edit_transaction"),
    path(
        "transaction/<int:pk>/delete/",
        views.delete_transaction,
        name="delete_transaction",
    ),
]
