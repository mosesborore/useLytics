from django import forms

from .models import Client, Invoice, InvoiceItem


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("created_at", "user")


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ("user", "created_at", "updated_at", "total_amount", "invoice_number")


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ("description", "quantity", "unit_price")
