from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
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
    today = timezone.now().date()

    transactions = Transaction.objects.filter(
        Q(date__month=today.month) & Q(date__year=today.year),
    )
    return transactions


def get_total_expense_per_category_chart_data():
    """Get the chart attributes (labels and data)"""
    qs = (
        Transaction.objects.filter(type="expense")
        .values("category__name")
        .annotate(total=Sum("amount"))
    )
    labels = []
    data = []

    for item in qs:
        labels.append(item.get("category__name"))
        data.append(item.get("total"))

    return {
        "total_expense_per_category": {
            "labels": labels,
            "data": data,
        },
    }


def get_total_income_and_total_expense_data():
    qs = (
        Transaction.objects.filter(date__year=timezone.now().year)
        .annotate(month=TruncMonth("date"))
        .values("month", "type")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    # Prepare data
    labels = []
    income_data = []
    expense_data = []

    months_seen = set()

    for item in qs:
        month_str = item["month"].strftime("%b")
        if month_str not in months_seen:
            labels.append(month_str)
            months_seen.add(month_str)

        if item["type"] == "income":
            income_data.append(float(item["total"]))
        else:
            expense_data.append(float(item["total"]))

    return {
        "total_income_and_total_expense": {
            "labels": labels,
            "income_data": income_data,
            "expense_data": expense_data,
        }
    }


def get_category_total_proportions():
    qs = (
        Transaction.objects.filter(
            date__month=timezone.now().month,
            date__year=timezone.now().year,
            type="expense",
        )
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    total = (
        Transaction.objects.filter(
            date__month=timezone.now().month,
            date__year=timezone.now().year,
            type="expense",
        )
        .aggregate(total_expense=Sum("amount"))
        .get("total_expense", 0)
    )

    if not total:
        return None

    records = []
    margin_left_offset = 0

    for idx, category_item in enumerate(qs):
        margin_left_offset = 0 if idx == 0 else margin_left_offset

        category_total = category_item.get("total", 0)
        # what proportion does it occupy in the overall `total`
        proportion = round((category_total / total) * 100)

        records.append(
            {
                "name": category_item.get("category__name"),
                "total": category_total,
                "proportion": proportion,
                "margin_offset": margin_left_offset,  # margin-left
            }
        )
        margin_left_offset += proportion

    return records
