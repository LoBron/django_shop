from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_catalog, name='catalog_home'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('product/<slug:prod_slug>/', views.ProductDetail.as_view(), name='product'),
    # path('category/<slug:cat_slug>/<slug:prod_slug>/', views.ProductDetail.as_view(), name='product'),
]
