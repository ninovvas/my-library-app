from django.core.validators import MaxLengthValidator
from django.db import models

# Create your models here.

class Book(models.Model):

    MAX_TITLE_LENGTH = 250
    MAX_ISBN10_LENGTH = 10
    MAX_ISBN13_LENGTH = 13

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH
    )

    isbn10 = models.CharField(
        max_length=MAX_ISBN10_LENGTH,
        validators=(
            #MaxLengthValidator(MAX_ISBN10_LENGTH)
        )
    )

    isbn13 = models.CharField(
        max_length=MAX_ISBN13_LENGTH,
        validators=(
            #MaxLengthValidator(MAX_ISBN13_LENGTH)
        )
    )