from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Equipment(models.Model):
    TYPES = (
        ('eletrodomestico', 'Eletrodoméstico'),
        ('eletronico', 'Eletrônico'),
        ('veiculo', 'Veículo'),
        ('outro', 'Outro'),
    )

    name = models.CharField('Nome', max_length=100)
    type = models.CharField('Tipo', max_length=20, choices=TYPES)
    brand = models.CharField('Marca', max_length=100)
    model = models.CharField('Modelo', max_length=100)
    serial_number = models.CharField('Número de Série', max_length=100, blank=True)
    purchase_date = models.DateField('Data de Compra', null=True, blank=True)
    notes = models.TextField('Observações', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Proprietário')
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.brand} {self.model}'

    def get_absolute_url(self):
        return reverse('maintenance:equipment_detail', kwargs={'pk': self.pk})

class MaintenanceOrder(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    )

    PRIORITY_CHOICES = (
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    )

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Equipamento')
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='concluida')
    priority = models.CharField('Prioridade', max_length=20, choices=PRIORITY_CHOICES, default='media')
    service_provider = models.CharField('Empresa Prestadora do Serviço', max_length=200, blank=True)
    completion_date = models.DateField('Data da Manutenção', null=True, blank=True)
    cost = models.DecimalField('Custo', max_digits=10, decimal_places=2, null=True, blank=True)
    warranty_expiration = models.DateField('Data de Vencimento da Garantia', null=True, blank=True)
    warranty_terms = models.TextField('Termos da Garantia', blank=True)
    invoice_number = models.CharField('Número da Nota Fiscal', max_length=50, blank=True)
    invoice_file = models.FileField('Nota Fiscal (PDF/Imagem)', upload_to='invoices/', null=True, blank=True)
    notes = models.TextField('Observações', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Criado por')
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Ordem de Manutenção'
        verbose_name_plural = 'Ordens de Manutenção'
        ordering = ['-completion_date']

    def __str__(self):
        return f'{self.equipment} - {self.service_provider} - {self.completion_date}'

    def get_absolute_url(self):
        return reverse('maintenance:order_detail', kwargs={'pk': self.pk})

class MaintenanceImage(models.Model):
    order = models.ForeignKey(MaintenanceOrder, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Imagem', upload_to='maintenance_images/')
    description = models.CharField('Descrição', max_length=200, blank=True)
    uploaded_at = models.DateTimeField('Data de Upload', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem da Manutenção'
        verbose_name_plural = 'Imagens da Manutenção'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'Imagem de {self.order}' 