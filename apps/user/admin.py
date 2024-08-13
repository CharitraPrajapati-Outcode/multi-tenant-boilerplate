from django.contrib import admin
from django import forms

from apps.user.models import User, UserProfile


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deleted_at'].required = False  # Ensure deleted_at is optional


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password', 'deleted_at')
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'deleted_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)

admin.site.register(UserProfile)
