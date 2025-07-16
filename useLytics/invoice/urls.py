from django.urls import path

from .views import (add_invoice_item, create_client, create_invoice, dashboard,
                    delete_invoice, edit_invoice, index, invoice_details)

app_name = "invoice"

urlpatterns = [
    path("", index, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("invoices/<int:pk>/", invoice_details, name="details"),
    path("invoices/", create_invoice, name="create_invoice"),
    path("invoices/<int:invoice_id>", edit_invoice, name="edit_invoice"),
    path("<int:invoice_id>/items/", add_invoice_item, name="add-items"),
    path("invoices/<int:invoice_id>/delete", delete_invoice, name="delete"),
    path("invoices/clients/", create_client, name="create_client"),
]
