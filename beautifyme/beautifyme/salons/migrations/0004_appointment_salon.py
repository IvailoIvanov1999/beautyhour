# Generated by Django 5.0.3 on 2024-04-01 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salons', '0003_appointment_delete_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='salon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='salons.salon'),
            preserve_default=False,
        ),
    ]
