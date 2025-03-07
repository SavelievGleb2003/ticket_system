from tkinter.font import names

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('login/', views.user_login, name='login')
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/<int:profile_id>/', views.different_user_profile, name='different_user_profile'),
    path('password-change/', views.my_PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password-reset/', views.my_PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.my_PasswordResetConfirmView.as_view(), name='password_reset_confirm' ),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit'),

]