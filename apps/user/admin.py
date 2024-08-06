from django.contrib import admin

from apps.user.models import User, UserProfile


admin.site.register(User)
admin.site.register(UserProfile)
