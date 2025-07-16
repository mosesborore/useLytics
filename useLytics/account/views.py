from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm


def home_view(request: HttpRequest):
    return redirect("accounts:create_account")


def login_view(request: HttpRequest):
    form = LoginForm()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        credentials = {"email": email, "password": password}
        user = authenticate(request, **credentials)

        if user:
            login(request, user)
            messages.success(request, "Successful login. Welcome")
            return redirect("invoice:home")
        messages.error(request, "Wrong Credentials. Try again")

    return render(request, "account/create_account.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")
