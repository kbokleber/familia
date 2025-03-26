from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
import json
from maintenance.models import Equipment, MaintenanceOrder

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Contagem de manutenções por status
        context['pending_count'] = MaintenanceOrder.objects.filter(
            created_by=user,
            status='pendente'
        ).count()

        context['in_progress_count'] = MaintenanceOrder.objects.filter(
            created_by=user,
            status='em_andamento'
        ).count()

        context['completed_count'] = MaintenanceOrder.objects.filter(
            created_by=user,
            status='concluida'
        ).count()

        # Total de equipamentos
        context['equipment_count'] = Equipment.objects.filter(
            owner=user
        ).count()

        # Últimas 5 manutenções realizadas
        context['recent_maintenance'] = MaintenanceOrder.objects.filter(
            created_by=user
        ).order_by('-completion_date', '-created_at')[:5]

        # Dados para o gráfico de custos
        months = []
        costs = []
        now = timezone.now()
        for i in range(6):
            date = now - timedelta(days=30 * i)
            month_orders = MaintenanceOrder.objects.filter(
                created_by=user,
                status='concluida',
                completion_date__year=date.year,
                completion_date__month=date.month
            )
            total_cost = sum(order.cost or 0 for order in month_orders)
            months.insert(0, date.strftime('%b/%Y'))
            costs.insert(0, float(total_cost))

        context['cost_months'] = json.dumps(months)
        context['monthly_costs'] = json.dumps(costs)

        return context 