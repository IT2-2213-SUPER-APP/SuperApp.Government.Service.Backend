from django.urls import path
from .views import UserRegistrationView, UserProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# THIS APP_NAME HELPS DJANGO DISTINGUISH BETWEEN APP NAMESPACES
app_name = 'users'

urlpatterns = [
    # REGISTRATION ENDPOINT
    path('register/', UserRegistrationView.as_view(), name='register'),

    # JWT TOKEN ENDPOINTS
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # USER PROFILE ENDPOINT
    path('profile/', UserProfileView.as_view(), name='profile'),
]
