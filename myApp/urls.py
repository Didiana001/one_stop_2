from . import views

from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    # path("test_openai/", views.test_openai, name="test_openai"),
]
# test_openai_connection