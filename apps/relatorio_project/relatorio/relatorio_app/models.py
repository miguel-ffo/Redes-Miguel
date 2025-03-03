from django.db import models

class Cliente(models.Model):
    class Meta:
        # Define o banco de dados que esse modelo usará
        db_table = 'clientes'  # Nome da tabela do cliente no banco de dados
        app_label = 'relatorio'
        managed = False  # Isso indica que o modelo não deve criar a tabela, já que ela existe no banco de dados

    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    criado_em = models.DateTimeField()

    def __str__(self):
        return self.nome
