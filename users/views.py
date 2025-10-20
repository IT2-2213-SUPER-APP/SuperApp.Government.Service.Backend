from rest_framework import generics, permissions
from .models import User
from .serializers import UserRegistrationSerializer, UserProfileSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows any user (anonymous) to create a new account.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # ANYONE CAN REGISTER

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the profile of the currently authenticated user.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # ONLY LOGGED-IN USERS CAN ACCESS

    def get_object(self):
        """
        Override the default `get_object` to return the current user's profile.
        This ensures users can only see and edit their own data.
        """
        return self.request.user
