from django.urls import path
from .views import dashboard_view
from .views import home

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("",home,name="home"),
]
