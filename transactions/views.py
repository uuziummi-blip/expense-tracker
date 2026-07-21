from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import CategoryForm, TransactionForm
from .models import Transaction


@login_required
def dashboard(request):
    # 1. Calculate Total Income
    income_dict = Transaction.objects.filter(
        user=request.user, category__type="Income"
    ).aggregate(Sum("amount"))
    total_income = income_dict["amount__sum"] or 0

    # 2. Calculate Total Expense
    expense_dict = Transaction.objects.filter(
        user=request.user, category__type="Expense"
    ).aggregate(Sum("amount"))
    total_expense = expense_dict["amount__sum"] or 0

    # 3. Calculate Balance
    balance = total_income - total_expense

    # 4. Get the 5 most recent transactions
    recent_transactions = Transaction.objects.filter(user=request.user).order_by(
        "-date", "-created_at"
    )[:5]

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
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
    transactions = Transaction.objects.filter(user=request.user).order_by(
        "-date", "-created_at"
    )
    return render(
        request, "transactions/transaction_list.html", {"transactions": transactions}
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
