# Generated by Django 5.0.2 on 2024-04-09 03:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_remove_medico_box_box_medico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='medico',
        ),
        migrations.AddField(
            model_name='medico',
            name='box',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.box'),
        ),
    ]
