from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'token', 'registered_at')
    list_filter = ('is_staff', 'is_active', 'registered_at')
    search_fields = ('username', 'email')
    readonly_fields = ('registered_at', 'token')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('token', 'registered_at'),
        }),
    )