from django.db.models import Q, Sum
from django.utils import timezone

from .models import Transaction


def get_stats(transactions=None):
    """Get data to display in the dashboard page"""

    stats = {}
    if not transactions:
        stats = {
            "total_expense": 0.0,
            "total_income": 0.0,
        }

    else:
        total_expense = (
            transactions.filter(type="expense")
            .aggregate(total_expense=Sum("amount"))
            .get("total_expense", 0)
        )
        total_income = (
            transactions.filter(type="income")
            .aggregate(total_income=Sum("amount"))
            .get("total_income")
        )
        stats = {
            "total_expense": total_expense if total_expense else 0,
            "total_income": total_income if total_income else 0,
        }
    return stats


def get_current_week_transactions():
    """Gets the current week transactions"""

    today = timezone.now()
    today_weekday = today.weekday()

    start_week_date = today - timezone.timedelta(days=today_weekday)
    end_week_date = today + timezone.timedelta(days=6 - today_weekday)

    transactions = Transaction.objects.filter(
        Q(date__gte=start_week_date) & Q(date__lte=end_week_date),
    )
    return transactions


def get_current_month_transactions():
    """Gets the current month transactions"""
    from calendar import monthrange

    today = timezone.now().date()

    month = today.month
    year = today.year
    end_month_day = monthrange(year, month)[1]

    start_date = timezone.datetime(year, month, 1).date()
    end_date = timezone.datetime(year, month, end_month_day).date()

    transactions = Transaction.objects.filter(
        Q(date__gte=start_date) & Q(date__lte=end_date),
    )
    return transactions
