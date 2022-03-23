from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_catalog, name='catalog_home'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
]
