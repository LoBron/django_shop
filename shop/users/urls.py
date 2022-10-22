from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    # path('', include('django.contrib.auth.urls')),
]
