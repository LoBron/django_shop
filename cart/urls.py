from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<slug:prod_slug>/', views.cart_add, name='cart_add'),
    path('remove/<slug:prod_slug>/', views.cart_remove, name='cart_remove')
]