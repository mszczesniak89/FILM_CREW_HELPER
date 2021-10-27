from django.urls import path
from .views import SignUpView, Login, PasswordResetView, PasswordResetDone, EditUser, validate_username

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', Login.as_view(redirect_authenticated_user=True), name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('edit_user/', EditUser.as_view(), name='edit_user'),
    path('validate_username', validate_username, name='validate_username')
]
