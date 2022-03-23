from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_catalog, name='catalog_home'),
    path('#', views.show_category, name='category'),
]
