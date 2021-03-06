from django.contrib import admin

# Register your models here.
from MyLibrary.accounts.models import Profile, AppUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(AppUser)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser')