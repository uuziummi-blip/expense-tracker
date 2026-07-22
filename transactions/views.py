from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, TransactionForm
from .models import Transaction, UserBalance
from django.core.paginator import Paginator
from django.core.cache import cache

# 1. Add this to your imports at the top
from django.core.cache import cache


@login_required
def dashboard(request):
    # 1. Get the data from the database
    user_balance, created = UserBalance.objects.get_or_create(user=request.user)
    recent_transactions = Transaction.objects.filter(user=request.user).order_by(
        "-date", "-created_at"
    )[:5]

    # 2. Map the data EXACTLY to the variable names your HTML is looking for
    context = {
        "total_income": user_balance.total_income,
        "total_expense": user_balance.total_expense,
        "balance": user_balance.balance,
        "recent_transactions": recent_transactions,
    }

    return render(request, "transactions/dashboard.html", context)


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Category added successfully!")
            return redirect("dashboard")
    else:
        form = CategoryForm()

    return render(
        request, "transactions/form.html", {"form": form, "title": "Add Category"}
    )


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added successfully!")
            return redirect("dashboard")
    else:
        form = TransactionForm(user=request.user)

    return render(
        request, "transactions/form.html", {"form": form, "title": "Add Transaction"}
    )


@login_required
def transaction_list(request):
    # 1. Fetch all transactions just like before
    all_transactions = Transaction.objects.filter(user=request.user).order_by(
        "-date", "-created_at"
    )

    # 2. Tell the Paginator to group them into chunks of 10
    paginator = Paginator(all_transactions, 10)

    # 3. Look at the URL to see what page the user clicked (e.g., /transactions/?page=2)
    # If there is no '?page=' in the URL, it defaults to None
    page_number = request.GET.get("page")

    # 4. Get only the 10 transactions for that specific page
    page_obj = paginator.get_page(page_number)

    # 5. Send 'page_obj' to the template instead of the full list
    return render(
        request, "transactions/transaction_list.html", {"transactions": page_obj}
    )


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = TransactionForm(
            request.POST, request.FILES, instance=transaction, user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully!")
            return redirect("transaction_list")
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(
        request, "transactions/form.html", {"form": form, "title": "Edit Transaction"}
    )


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        transaction.delete()
        messages.success(request, "Transaction deleted successfully!")
        return redirect("transaction_list")
    return render(
        request, "transactions/delete_confirm.html", {"transaction": transaction}
    )
