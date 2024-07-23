from django.urls import path

from authorization.views import Login

urlpatterns = [
    path("login", Login.as_view(), name="login"),
]
