from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    nome_usuario = models.CharField(max_length=45)
    imagem_codificada = models.CharField(max_length=5000)
    nivel_acesso = models.IntegerField()


