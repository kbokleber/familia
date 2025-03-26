# Generated by Django 5.0.1 on 2025-03-24 14:38

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
            name='DashboardPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_pending_maintenance', models.BooleanField(default=True, verbose_name='Mostrar Manutenções Pendentes')),
                ('show_equipment_stats', models.BooleanField(default=True, verbose_name='Mostrar Estatísticas de Equipamentos')),
                ('show_cost_analysis', models.BooleanField(default=True, verbose_name='Mostrar Análise de Custos')),
                ('show_upcoming_maintenance', models.BooleanField(default=True, verbose_name='Mostrar Próximas Manutenções')),
                ('days_to_alert', models.IntegerField(default=7, verbose_name='Dias para Alertar')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Preferência do Dashboard',
                'verbose_name_plural': 'Preferências do Dashboard',
            },
        ),
    ]
