# Generated by Django 5.0.2 on 2024-03-16 17:57

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(10)])),
                ('nombre_completo', models.CharField(max_length=200)),
                ('especialidad', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'medico',
                'verbose_name_plural': 'medicos',
                'db_table': 'medicos',
            },
        ),
        migrations.CreateModel(
            name='AtencionMedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=9)),
                ('hora_inicio', models.TimeField()),
                ('hora_termino', models.TimeField()),
                ('box', models.CharField(max_length=50)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.medico')),
            ],
            options={
                'verbose_name': 'atencion medica',
                'verbose_name_plural': 'atenciones medica',
                'db_table': 'atencion_medica',
            },
        ),
        migrations.CreateModel(
            name='ReservaAtencion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('atencionmedica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.atencionmedica')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='atencionmedica',
            name='usuario',
            field=models.ManyToManyField(through='hospital.ReservaAtencion', to=settings.AUTH_USER_MODEL),
        ),
    ]
