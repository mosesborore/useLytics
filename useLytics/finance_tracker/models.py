from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        (_("expense"), "Expense"),
        (_("income"), "Income"),
    )

    description = models.CharField(_("Description"), max_length=128)
    date = models.DateField(_("Date"))
    amount = models.FloatField(_("Amount"), default=0.0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    type = models.CharField(
        _("Transaction Type"),
        max_length=50,
        choices=TRANSACTION_TYPE,
        default="expense",
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{ self.description} - {self.date} - {self.amount}"
