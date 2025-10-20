from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles password validation and hashing.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        # FIELDS REQUIRED FOR CREATING A USER.
        # NOTE: WE USE EMAIL AS THE PRIMARY IDENTIFIER.
        fields = (
            'email', 'password', 'first_name', 'last_name', 'middle_name', 'iin',
            'date_of_birth', 'sex', 'status', 'phone_number', 'identity_document_number'
        )

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            iin=validated_data['iin'],
            date_of_birth=validated_data['date_of_birth'],
            sex=validated_data['sex'],
            status=validated_data['status'],
            phone_number=validated_data['phone_number'],
            identity_document_number=validated_data['identity_document_number'],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying and updating a user's profile.
    Some fields are made read-only to prevent users from changing them.
    """
    class Meta:
        model = User
        # ALL FIELDS FROM THE MODEL ARE INCLUDED, BUT SOME WILL BE READ-ONLY.
        fields = '__all__'
        read_only_fields = (
            'id', 'email', 'iin', 'date_of_birth', 'is_staff', 'is_superuser',
            'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions',
            'deleted'
        )
