# Generated by Django 5.0.2 on 2024-04-08 04:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_remove_reservaatencion_atencionmedica_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='medico',
        ),
        migrations.AddField(
            model_name='medico',
            name='box',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='hospital.box'),
            preserve_default=False,
        ),
    ]
