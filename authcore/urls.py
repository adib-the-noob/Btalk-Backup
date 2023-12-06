from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('verify-otp/', views.OtpVerifyView.as_view(), name='verify'),
    path('logout/', views.logout_view, name='logout'),

    # forgot password
    path('forgot-password-otp-request/', views.ForgotPasswordOtpRequestView.as_view(), name='forgot-password-otp-request'),
    path('forgot-password-otp-verify/', views.ForgotPasswordOtpVerifyView.as_view(), name='forgot-password-otp-verify'),
    path('forgot-password-reset/', views.ResetPasswordView.as_view(), name='forgot-password-reset'),

    path('resend-otp/', views.resend_otp, name='resend-otp'),

    # profile picture
    path('profile-picture/', views.ProfilePictureView.as_view(), name='profile-picture'),
]
