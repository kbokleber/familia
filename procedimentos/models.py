from django.db import models

class Procedimento(models.Model):
    titulo = models.CharField(max_length=200)
    # ... outros campos existentes ...

class DocumentoProcedimento(models.Model):
    procedimento = models.ForeignKey(Procedimento, on_delete=models.CASCADE, related_name='documentos')
    arquivo = models.FileField(upload_to='procedimentos/documentos/')
    nome = models.CharField(max_length=200)
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Documento do Procedimento'
        verbose_name_plural = 'Documentos do Procedimento' 