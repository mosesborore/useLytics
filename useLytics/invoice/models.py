from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from account.models import User


def date_after(duration: int):
    return timezone.now().date() + timedelta(days=duration)


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    date_issued = models.DateField(default=timezone.now)
    due_date = models.DateField(default=date_after(14))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Unpaid")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoices"
        ordering = ["-created_at"]

    @property
    def line_total(self):
        return sum([item.total_price for item in self.items.all()])  # type: ignore


from decimal import Decimal


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(_("Quantity"), max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(_("Unit Price"), max_digits=10, decimal_places=2)
    total_price = models.DecimalField(
        _("Unit Price"), max_digits=10, decimal_places=2, default=Decimal(0.0)
    )

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
