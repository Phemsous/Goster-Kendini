from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Video, Job, Comment

# Özel User modelimizi admin panelinde düzgün görmek için
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Tabloları tek tek kaydediyoruz
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Video)
admin.site.register(Job)
admin.site.register(Comment)