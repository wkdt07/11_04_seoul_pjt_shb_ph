# Generated by Django 4.2.13 on 2024-05-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0001_initial'),
        ('accounts', '0002_alter_user_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='savings',
            field=models.ManyToManyField(blank=True, related_name='users', to='compare.saving'),
        ),
    ]
