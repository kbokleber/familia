from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenanceimage',
            name='maintenance_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='maintenance.maintenanceorder', verbose_name='Ordem de Manutenção'),
        ),
    ] 