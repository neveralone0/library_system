from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    # shows in admin panel
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password', 'profile')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),
    )

    # superuser register
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'fullname', 'password1', 'password2')}),
    )

    search_fields = ('email',)
    ordering = ('full_name',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)