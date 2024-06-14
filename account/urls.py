from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # previous login url
    # path('login/', views.user_login, name='login'),
    # Login / logout urls
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # change the password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('', views.dashboard, name='dashboard'),
]