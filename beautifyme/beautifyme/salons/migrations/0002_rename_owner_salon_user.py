# Generated by Django 5.0.3 on 2024-04-01 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salons', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salon',
            old_name='owner',
            new_name='user',
        ),
    ]
