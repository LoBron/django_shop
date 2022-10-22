from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='catalog_home'),
    path('category/<slug:cat_slug>/', views.ProductCategoryList.as_view(), name='category'),
    path('product/<slug:prod_slug>/<int:prod_id>/', views.ProductDetail.as_view(), name='product'),
    path('search/', views.Search.as_view(), name='search'),
    path('filter/', views.ProductFilterList.as_view(), name='filter'),
    # path('category/<slug:cat_slug>/<slug:prod_slug>/', views.ProductDetail.as_view(), name='product'),
]
