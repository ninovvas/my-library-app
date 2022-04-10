from django.contrib import admin
#https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
# Register your models here.
from MyLibrary.main.models import Book, Author, Publisher


@admin.register(Book)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Publisher)
class ProfileAdmin(admin.ModelAdmin):
    pass