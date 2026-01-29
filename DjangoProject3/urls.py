from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path( "dashboard/", include("dashboard_app.urls")),
    path("",include("dashboard_app.urls")) ,

]