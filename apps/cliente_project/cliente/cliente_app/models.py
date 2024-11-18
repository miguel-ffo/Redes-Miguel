from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome