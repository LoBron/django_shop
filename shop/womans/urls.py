from django.urls import path
from . import views

urlpatterns = [
    path('', views.womens_home, name='womens'),
    path('post/<int:pk>', views.WomensDetailView.as_view(), name='post'),
]
