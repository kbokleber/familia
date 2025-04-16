from django.db import models

class SystemConfig(models.Model):
    key = models.CharField('Chave', max_length=50, unique=True)
    value = models.TextField('Valor')
    description = models.TextField('Descrição', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'
        ordering = ['key']

    def __str__(self):
        return self.key 