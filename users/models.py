import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class User(AbstractUser, SafeDeleteModel):
    """
    Custom User model extending Django's AbstractUser and SafeDeleteModel.
    This model is the single source of truth for user authentication and basic profile info.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, help_text="Required. Used for login and notifications.")

    # Override the username field to not be unique, as email will be the main identifier.
    # We keep it for compatibility with Django's ecosystem but make it non-essential.
    username = models.CharField(
        max_length=150,
        unique=False,
        help_text="Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['email']
