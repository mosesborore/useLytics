from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRefresh

from account.models import User
from invoice.forms import ClientForm, InvoiceForm, InvoiceItemForm
from invoice.models import Invoice, InvoiceItem


@login_required
def index(request: HttpRequest):
    form = InvoiceForm()
    client_form = ClientForm()

    return render(
        request,
        "invoice/index.html",
        {"form": form, "client_form": client_form},
    )


@login_required
def dashboard(request: HttpRequest):
    invoices = Invoice.objects.select_related("client").prefetch_related("items")

    stats = {}

    total_revenue = invoices.aggregate(total_revenue=Sum("items__total_price")).get(
        "total_revenue", 0.0
    )
    stats["paid_invoices"] = invoices.filter(status="unpaid").count()
    stats["overdue"] = invoices.filter(due_date__lt=datetime.today().date()).count()

    stats["total_revenue"] = total_revenue
    return render(
        request,
        "invoice/dashboard.html",
        {"invoices": invoices, "stats": stats},
    )


def invoice_details(request: HttpRequest, pk):
    """View the invoice details which has the given `pk`"""
    # invoice = get_object_or_404(Invoice, pk=pk)
    invoice = Invoice.objects.filter(pk=pk).select_related("client", "user").first()

    if not invoice:
        raise Http404("Invoice not found that has the given id. May be deleted.")
    items = invoice.items.all()  # type: ignore

    return render(
        request, "invoice/invoice_details.html", {"invoice": invoice, "items": items}
    )


@login_required
@require_POST
def create_invoice(request: HttpRequest):
    """View to create a new invoice"""
    form = InvoiceForm(request.POST)
    form_items = InvoiceItemForm()
    user = request.user

    if form.is_valid():
        invoice_instance = form.save(commit=False)
        invoice_instance.user = user
        invoice_instance.save()

        messages.success(request, "invoice added successfully")
        return render(
            request,
            "invoice/widgets/invoice_item_form.html",
            {
                "form_items": form_items,
                "invoice": invoice_instance,
                "items": invoice_instance.items.all(),
            },
        )
    messages.error(request, "Unable to save invoice.")
    errors = form.errors.as_text
    form = InvoiceForm(initial=request.POST.dict())

    return render(
        request,
        "invoice/index.html",
        {"form": form, "errors": errors},
    )


@require_POST
def add_invoice_item(request: HttpRequest, invoice_id: int):
    """
    View that adds invoice item to invoice with the given `invoice_id`

    Accepts POST requests only
    """
    form = InvoiceItemForm(request.POST)
    form_items = InvoiceItemForm()
    invoice = Invoice.objects.get(id=invoice_id)

    if form.is_valid():
        if invoice:
            item = form.save(commit=False)
            item.invoice = invoice
            item.save()
            # invoice.refresh_from_db()
            items = invoice.items.all()  # type: ignore

            messages.success(request, "New invoice item added")
            return render(
                request,
                "invoice/widgets/invoice_item_form.html",
                {
                    "form_items": form_items,
                    "items": items,
                    "invoice": invoice,
                },
            )
        else:
            messages.error(request, "Unable to add item. Invoice not found.")

    errors = form.errors.as_text()
    messages.error(request, "Unable to save")

    form_items = InvoiceItemForm(initial=request.POST.dict())
    items = invoice.items.all()  # type: ignore
    return render(
        request,
        "invoice/widgets/invoice_item_form.html",
        {
            "form_items": form_items,
            "items": items,
            "invoice": invoice,
            "errors": errors,
        },
    )


def edit_invoice(request: HttpRequest, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == "POST":
        form = InvoiceForm(
            request.POST,
            instance=invoice,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice updated")
        else:
            messages.error(
                request, f"Unable to update invoice {str(form.errors.as_text)}"
            )
        return HttpResponseClientRefresh()

    form = InvoiceForm(instance=invoice)
    return render(
        request, "invoice/edit_invoice.html", {"form": form, "invoice": invoice}
    )


@csrf_exempt
def delete_invoice(request: HttpRequest, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    messages.success(request, "Invoice deleted")

    return HttpResponseClientRefresh()


@require_POST
def create_client(request: HttpRequest):
    form = ClientForm(request.POST)
    if form.is_valid():
        user = User.objects.first()
        client_instance = form.save(commit=False)
        client_instance.user = user
        client_instance.save()
        messages.success(request, "Client Saved")
    else:
        messages.error(request, f"Unable to save cliend. {str(form.errors.as_text)}")

    return HttpResponseClientRefresh()
