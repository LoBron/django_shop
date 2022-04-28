from django.urls import path
from . import views, add_data_to_database

urlpatterns = [
    path('', views.ProductList.as_view(), name='catalog_home'),
    path('category/<slug:cat_slug>/', views.ProductCategoryList.as_view(), name='category'),
    path('product/<slug:prod_slug>/<int:prod_id>/', views.ProductDetail.as_view(), name='product'),
    path('search/', views.Search.as_view(), name='search'),
    path('filter/', views.ProductFilterList.as_view(), name='filter'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('save/', add_data_to_database.form_save, name='save'),
    path('save_categories/', add_data_to_database.categories_save, name='save_cats')

    # path('category/<slug:cat_slug>/<slug:prod_slug>/', views.ProductDetail.as_view(), name='product'),
]
