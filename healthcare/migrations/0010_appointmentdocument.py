from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0009_alter_medicalprocedure_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='appointment_documents/', verbose_name='Arquivo')),
                ('name', models.CharField(max_length=255, verbose_name='Nome do Arquivo')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Enviado em')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='healthcare.medicalappointment', verbose_name='Consulta')),
            ],
            options={
                'verbose_name': 'Documento da Consulta',
                'verbose_name_plural': 'Documentos das Consultas',
                'ordering': ['-uploaded_at'],
            },
        ),
    ] 