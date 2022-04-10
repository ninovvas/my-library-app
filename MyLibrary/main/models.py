from django.core.validators import MinLengthValidator
from django.db import models
from MyLibrary.accounts.models import AppUser
from MyLibrary.common.validators import validate_only_letters
from cloudinary import models as cloudinary_models


class Author(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 150
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30

    # first_name = models.CharField(
    #     max_length=FIRST_NAME_MAX_LENGTH,
    #     validators=(
    #         MinLengthValidator(FIRST_NAME_MIN_LENGTH),
    #         validate_only_letters,
    #     )
    # )
    #
    # last_name = models.CharField(
    #     max_length=LAST_NAME_MAX_LENGTH,
    #     validators=(
    #         MinLengthValidator(LAST_NAME_MIN_LENGTH),
    #         validate_only_letters,
    #     )
    # )
    #
    # picture = models.URLField(
    #     null=True,
    #     blank=True,
    # )
    #
    # salutation = models.CharField(
    #     max_length=10
    # )
    name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )


    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Publisher(models.Model):
    MAX_NAME_LENGTH = 30
    MAX_ADDRESS_LENGTH = 50

    publisher_name = models.CharField(max_length=MAX_NAME_LENGTH)

    address = models.CharField(
        max_length=MAX_ADDRESS_LENGTH,
        null=True,
        blank=True,
    )
    city = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )

    state_province = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    country = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    website = models.URLField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.publisher_name

class Book(models.Model):

    MAX_TITLE_LENGTH = 250
    MAX_ISBN10_LENGTH = 10
    MAX_ISBN13_LENGTH = 13
    MAX_LANGUAGE_LENGTH = 15

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH
    )

    isbn10 = models.CharField(
        max_length=MAX_ISBN10_LENGTH,
        validators=(
            MinLengthValidator(MAX_ISBN10_LENGTH),
        )
    )

    isbn13 = models.CharField(
        max_length=MAX_ISBN13_LENGTH,
        validators=(
            MinLengthValidator(MAX_ISBN13_LENGTH),
        )
    )

    language = models.CharField(
        max_length=MAX_LANGUAGE_LENGTH,
        null=True,
        blank=True,

    )

    page_count = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    start_read_date = models.DateField(
        null=True,
        blank=True,
    )

    end_read_date = models.DateField(
        null=True,
        blank=True,
    )

    read = models.BooleanField(
        default=False,
    )

    user_comment = models.TextField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    pubdate = models.DateField(
        auto_now_add=True,
    )

    #image = cloudinary_models.CloudinaryField('image')
    # image = models.ImageField(
    #     upload_to='images/',
    #     null=True,
    #     blank=True,
    # )

    image = models.URLField(
        null=True,
        blank=True,

    )

    authors = models.ManyToManyField(
        Author,
        editable=True,

    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title






