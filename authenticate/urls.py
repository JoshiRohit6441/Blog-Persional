from .views import RegisterView, VerifyView, ResendVerificationCOdeView, LoginView, UserProfileView, LogoutView, ForgotPasswordEmailView, ForgotPasswordVerifyView, ResetPasswordView, ResendResetPasswordVerificationView, UserListView, DeleteUserView, EditUserView, UpdateUserProfile
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<int:otp>/', VerifyView.as_view(), name='verify'),
    path('resend-verification-code/', ResendVerificationCOdeView.as_view(),
         name='resend-vverification-code/'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-profile/<int:id>',
         UpdateUserProfile.as_view(), name='update-profile'),
    # -----------------------forgot-password--------------------
    path('forgot-password-code/', ForgotPasswordEmailView.as_view(),
         name='forgot-password-code'),
    path('forgot-password-verify/<int:otp>/',
         ForgotPasswordVerifyView.as_view(), name='forgot'),
    path('reset-password/',
         ResetPasswordView.as_view(), name='reset-password'),
    path('resend-forgot-code/',
         ResendResetPasswordVerificationView.as_view(), name='resend-forgot-code'),
    #  -----------------------------admin--------------------------
    path('list-user/', UserListView.as_view(), name="list-users"),
    path('edit-user/', EditUserView.as_view(), name="edit-users"),
    path('Delete-user/', DeleteUserView.as_view(), name="delet-users"),

    # ------------------------------refresh-token----------------------------
    path('refresh-token/', TokenRefreshView.as_view(), name="refresh-token"),

]
