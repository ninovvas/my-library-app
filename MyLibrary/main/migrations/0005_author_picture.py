# Generated by Django 4.0.3 on 2022-04-12 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_book_end_read_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='picture',
            field=models.URLField(blank=True, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-UpHstLuRde04pBD5oaO6v8UQPoVPGSVpww&usqp=CAU', null=True),
        ),
    ]
