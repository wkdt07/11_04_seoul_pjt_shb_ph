# Generated by Django 4.2.13 on 2024-05-23 05:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('real_estate', '0003_rename_religion_realestate_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realestate',
            name='user',
        ),
        migrations.AddField(
            model_name='realestate',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='real_estates', to=settings.AUTH_USER_MODEL),
        ),
    ]