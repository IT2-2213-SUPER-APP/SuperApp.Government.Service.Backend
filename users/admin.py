from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'deleted')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'deleted')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Soft Delete', {'fields': ('deleted',)}),
    )
    # Add the 'deleted' field to the readonly fields if you don't want it to be editable in the admin
    readonly_fields = ('last_login', 'date_joined', 'deleted')
