from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    # If the user submits the form (POST request)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Creates the user in the database
            messages.success(
                request, "Account created successfully! You can now log in."
            )
            return redirect("login")
    # If the user is just loading the page (GET request)
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})
