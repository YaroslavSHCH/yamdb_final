from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email', 'first_name', 'last_name',
                    'role']
    exclude = ['password']
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    search_fields = ['username', 'email']
    list_filter = ['role', 'created_at']
    empty_value_display = '-пусто-'
