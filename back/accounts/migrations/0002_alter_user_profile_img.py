# Generated by Django 4.2.13 on 2024-05-21 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(default='images/user.png', upload_to='users/'),
        ),
    ]
