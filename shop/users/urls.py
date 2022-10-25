from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'confirm_email/',
        TemplateView.as_view(template_name='users/confirm_email.html'),
        name='confirm_email'
    ),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path(
        'invalid_verify/',
        TemplateView.as_view(template_name='users/invalid_verify.html'),
        name='invalid_verify'
    ),

    path('login/', LoginView.as_view(), name='login'),
    path('login/ajax/', LoginAjaxView.as_view(), name='login_ajax'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    # path('', include('django.contrib.auth.urls')),
]
