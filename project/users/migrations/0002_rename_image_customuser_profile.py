# Generated by Django 4.2.1 on 2023-05-30 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='image',
            new_name='profile',
        ),
    ]