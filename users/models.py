from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, SafeDeleteModel):
    """
    Custom User model for the government portal.
    Inherits from SafeDeleteModel for soft-deletion capabilities.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    # --- CHOICES ---
    class Sex(models.TextChoices):
        MALE = 'MALE', _('Male')
        FEMALE = 'FEMALE', _('Female')

    class Status(models.TextChoices):
        LOCAL = 'LOCAL', _('Local')
        MIGRANT = 'MIGRANT', _('Migrant')

    # --- OVERRIDE DEFAULT FIELDS ---
    username = None # WE WILL USE EMAIL AS THE UNIQUE IDENTIFIER
    email = models.EmailField(_('email address'), unique=True)

    # SET EMAIL AS THE USERNAME FIELD AND REQUIRE ESSENTIAL FIELDS
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS WILL STILL BE ENFORCED BY CREATESUPERUSER AND OUR FUTURE FORMS/SERIALIZERS
    REQUIRED_FIELDS = ['first_name', 'last_name', 'middle_name', 'iin', 'date_of_birth', 'sex', 'status', 'phone_number', 'identity_document_number']

    # --- CORE INFORMATION (REQUIRED) ---
    # WE ADD `NULL=TRUE` TO ALLOW DJANGO-GUARDIAN'S ANONYMOUS USER CREATION TO SUCCEED.
    middle_name = models.CharField(_("middle name"), max_length=150, null=True)
    iin = models.CharField(_("IIN (ИИН)"), max_length=12, unique=True, help_text=_("Individual Identification Number"), null=True)
    date_of_birth = models.DateField(_("date of birth"), null=True)
    sex = models.CharField(_("sex"), max_length=6, choices=Sex.choices, null=True)
    status = models.CharField(_("status"), max_length=7, choices=Status.choices, null=True)
    phone_number = models.CharField(_("primary phone number"), max_length=20, null=True)
    identity_document_number = models.CharField(_("identity document number"), max_length=20, unique=True, null=True)

    # --- ADDITIONAL INFORMATION (OPTIONAL) ---
    height = models.PositiveIntegerField(_("height in cm"), null=True, blank=True)
    weight = models.PositiveIntegerField(_("weight in kg"), null=True, blank=True)
    race = models.CharField(_("race"), max_length=50, blank=True)

    # USING JSONFIELD FOR FLEXIBLE MULTI-VALUE STORAGE AS A SIMPLE SOLUTION
    # A MORE NORMALIZED APPROACH WOULD BE A SEPARATE RELATED MODEL.
    additional_phone_numbers = models.JSONField(_("additional phone numbers"), default=list, blank=True, help_text=_("List of up to two additional phone numbers"))

    physical_address = models.TextField(_("physical address"), blank=True)

    # FOR MORE COMPLEX DATA, JSONFIELD IS A GOOD CHOICE FOR THIS MOCKUP
    marriage_status_info = models.JSONField(_("marriage status information"), default=dict, blank=True)
    children_info = models.JSONField(_("children information"), default=list, blank=True)

    # --- DOCUMENT IMAGES ---
    profile_picture = models.ImageField(_("profile picture"), upload_to='profile_pictures/', null=True, blank=True)
    identity_document_front = models.ImageField(_("identity document front"), upload_to='documents/identity/', null=True, blank=True)
    identity_document_back = models.ImageField(_("identity document back"), upload_to='documents/identity/', null=True, blank=True)
    driver_license_front = models.ImageField(_("driver license front"), upload_to='documents/drivers_license/', null=True, blank=True)
    driver_license_back = models.ImageField(_("driver license back"), upload_to='documents/drivers_license/', null=True, blank=True)
    driver_license_number = models.CharField(_("driver license number"), max_length=20, blank=True)

    objects = UserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name
        return self.email

    @property
    def get_full_name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
