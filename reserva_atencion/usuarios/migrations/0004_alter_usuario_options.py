# Generated by Django 5.0.2 on 2024-03-16 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_usuario_options_alter_usuario_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'verbose_name': 'usuario', 'verbose_name_plural': 'usuarios'},
        ),
    ]
