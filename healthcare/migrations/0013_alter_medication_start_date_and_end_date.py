from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0012_exam_alter_appointmentdocument_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='start_date',
            field=models.DateTimeField(verbose_name='Data e Hora de Início'),
        ),
        migrations.AlterField(
            model_name='medication',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data e Hora de Término'),
        ),
    ] 