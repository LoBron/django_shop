from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_catalog, name='catalog_home'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('product/<slug:prod_slug>/', views.ProductDetail.as_view(), name='product'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('category/<slug:cat_slug>/<slug:prod_slug>/', views.ProductDetail.as_view(), name='product'),
]
