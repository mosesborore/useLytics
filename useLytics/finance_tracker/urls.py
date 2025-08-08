from django.urls import path

from .views import (
    create_transaction_view,
    delete_transaction_view,
    filtered_transactions_view,
    get_progress_view,
    home_view,
)

app_name = "tracker"

urlpatterns = [
    path(
        "",
        home_view,
        name="home",
    ),
    path(
        "create/",
        create_transaction_view,
        name="create",
    ),
    path(
        "delete/<int:pk>",
        delete_transaction_view,
        name="delete",
    ),
    path("filter/", filtered_transactions_view, name="filter"),
    path("progress/", get_progress_view, name="progress"),
]
