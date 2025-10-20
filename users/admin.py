from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    """
    # USE THE DEFAULT USERADMIN FIELDSETS AND ADD OUR CUSTOM FIELDS
    # THIS PROVIDES A FAMILIAR AND FUNCTIONAL ADMIN INTERFACE
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Personal Information', {'fields': ('middle_name', 'iin', 'date_of_birth', 'sex', 'status')}),
        ('Contact Information', {'fields': ('phone_number', 'additional_phone_numbers', 'physical_address')}),
        ('Physical Attributes', {'fields': ('height', 'weight', 'race')}),
        ('Documents', {'fields': ('identity_document_number', 'driver_license_number')}),
        ('Family Information', {'fields': ('marriage_status_info', 'children_info')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('middle_name', 'iin', 'date_of_birth', 'sex', 'status', 'phone_number', 'identity_document_number')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'deleted')
    search_fields = ('email', 'first_name', 'last_name', 'iin')
    ordering = ('email',)

    # ADD THE 'DELETED' FIELD FROM DJANGO-SAFEDELETE TO THE LIST FILTER
    list_filter = BaseUserAdmin.list_filter + ('deleted',)
