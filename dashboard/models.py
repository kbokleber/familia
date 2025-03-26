from django.db import models
from django.contrib.auth.models import User
from maintenance.models import Equipment, MaintenanceOrder

class DashboardPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show_pending_maintenance = models.BooleanField('Mostrar Manutenções Pendentes', default=True)
    show_equipment_stats = models.BooleanField('Mostrar Estatísticas de Equipamentos', default=True)
    show_cost_analysis = models.BooleanField('Mostrar Análise de Custos', default=True)
    show_upcoming_maintenance = models.BooleanField('Mostrar Próximas Manutenções', default=True)
    days_to_alert = models.IntegerField('Dias para Alertar', default=7)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Preferência do Dashboard'
        verbose_name_plural = 'Preferências do Dashboard'

    def __str__(self):
        return f'Preferências de {self.user.username}' 