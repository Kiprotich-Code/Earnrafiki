from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ['email']
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'user_type')
    list_filter = ('is_staff', 'is_active', 'user_type')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'address', 'phone_no', 'user_type')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Password reset'), {'fields': ('password_reset_token', 'password_reset_expiry')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If object is new
            obj.set_password(form.cleaned_data.get('password1'))
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Override form to use the password fields
        form.base_fields['password'].widget = forms.PasswordInput(render_value=True)
        return form

admin.site.register(CustomUser, CustomUserAdmin)
