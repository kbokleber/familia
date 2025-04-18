# Generated by Django 4.2.20 on 2025-04-16 12:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('type', models.CharField(choices=[('eletronico', 'Eletrônico'), ('eletrodomestico', 'Eletrodoméstico'), ('movel', 'Móvel'), ('veiculo', 'Veículo'), ('outro', 'Outro')], default='outro', max_length=50, verbose_name='Tipo')),
                ('brand', models.CharField(blank=True, max_length=100, null=True, verbose_name='Marca')),
                ('model', models.CharField(blank=True, max_length=100, null=True, verbose_name='Modelo')),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Número de Série')),
                ('purchase_date', models.DateField(blank=True, null=True, verbose_name='Data de Compra')),
                ('notes', models.TextField(blank=True, verbose_name='Observações')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Proprietário')),
            ],
            options={
                'verbose_name': 'Equipamento',
                'verbose_name_plural': 'Equipamentos',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('em_andamento', 'Em Andamento'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')], default='concluida', max_length=20, verbose_name='Status')),
                ('priority', models.CharField(choices=[('baixa', 'Baixa'), ('media', 'Média'), ('alta', 'Alta'), ('urgente', 'Urgente')], default='media', max_length=20, verbose_name='Prioridade')),
                ('service_provider', models.CharField(blank=True, max_length=200, verbose_name='Empresa Prestadora do Serviço')),
                ('completion_date', models.DateField(blank=True, null=True, verbose_name='Data da Manutenção')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Custo')),
                ('warranty_expiration', models.DateField(blank=True, null=True, verbose_name='Data de Vencimento da Garantia')),
                ('warranty_terms', models.TextField(blank=True, verbose_name='Termos da Garantia')),
                ('invoice_number', models.CharField(blank=True, max_length=50, verbose_name='Número da Nota Fiscal')),
                ('invoice_file', models.FileField(blank=True, null=True, upload_to='invoices/', verbose_name='Nota Fiscal (PDF/Imagem)')),
                ('notes', models.TextField(blank=True, verbose_name='Observações')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maintenance.equipment', verbose_name='Equipamento')),
            ],
            options={
                'verbose_name': 'Ordem de Manutenção',
                'verbose_name_plural': 'Ordens de Manutenção',
                'ordering': ['-completion_date'],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='maintenance_images/', verbose_name='Imagem')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Descrição')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Upload')),
                ('maintenance_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='maintenance.maintenanceorder', verbose_name='Ordem de Manutenção')),
            ],
            options={
                'verbose_name': 'Imagem da Manutenção',
                'verbose_name_plural': 'Imagens da Manutenção',
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='EquipmentAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='equipment_attachments/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif'])], verbose_name='Arquivo')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Upload')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='maintenance.equipment', verbose_name='Equipamento')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Upload por')),
            ],
            options={
                'verbose_name': 'Anexo do Equipamento',
                'verbose_name_plural': 'Anexos do Equipamento',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
