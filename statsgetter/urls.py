from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('export_excel', views.export_excel, name="export-excel"),
]
