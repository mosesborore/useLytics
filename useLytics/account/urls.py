from django.urls import path

from account.views import home_view, login_view

app_name = "accounts"

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
]
