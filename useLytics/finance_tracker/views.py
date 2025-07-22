from django.contrib import messages
from django.db.models import Sum
from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from django_htmx.http import HttpResponseClientRefresh

from .forms import TransactionForm
from .models import Transaction
from .services import (
    get_stats,
    get_current_week_transactions,
    get_current_month_transactions,
)

template_folder = "finance_tracker"


def home_view(request: HttpRequest):
    transactions = Transaction.objects.all()

    stats = get_stats(transactions)

    form = TransactionForm(initial={"date": timezone.now().date()})
    context = {
        "form": form,
        "transactions": transactions,
        "stats": stats,
    }
    return render(request, f"{template_folder}/index.html", context)


@require_POST
def create_transaction_view(request: HttpRequest):
    """View to create new transaction. Accepts only POST requests"""
    form = TransactionForm(request.POST)
    print(request.POST)
    message = ""
    transaction = None
    if form.is_valid():
        transaction_obj = form.save(commit=False)
        transaction_obj.save()
        transaction = transaction_obj
        message = "Transaction Saved"
    else:
        message = str(form.errors.as_text)
    form = TransactionForm(initial={"date": timezone.now().date()})

    context = {
        "form": form,
        "transaction": transaction,
        "message": message,
    }

    return render(request, f"{template_folder}/create.html", context)


def edit_transaction(request: HttpRequest):
    pass


@require_POST
def delete_transaction_view(request: HttpRequest, pk: int):
    transaction = Transaction.objects.filter(pk=pk).first()
    print(request.method, transaction)
    if not transaction:
        messages.error(request, "Transaction Not Found")
    else:
        transaction.delete()
        messages.success(request, "Transaction Deleted")

    return HttpResponseClientRefresh()


def add_category(request: HttpRequest):
    pass


@require_GET
def filtered_transactions_view(request: HttpRequest):
    filter_by = ""
    query_string = request.META.get("QUERY_STRING", "")

    if query_string:
        filter_by = query_string.split("=")[1].strip().lower()

    transactions = None

    if filter_by == "week":
        transactions = get_current_week_transactions()
    elif filter_by == "month":
        transactions = get_current_month_transactions()
    else:
        transactions = Transaction.objects.filter(date=timezone.now().date())

    stats = get_stats(transactions)

    print(stats)
    context = {"transactions": transactions, "stats": stats}

    return render(request, f"{template_folder}/filter_results.html", context)
