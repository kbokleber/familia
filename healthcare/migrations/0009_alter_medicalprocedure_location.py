# Generated by Django 4.2.10 on 2024-03-28 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0008_proceduredocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalprocedure',
            name='location',
            field=models.CharField(blank=True, max_length=200, verbose_name='Local'),
        ),
    ] 