from django.db import models

class AgendaTributaria(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.data.strftime('%d/%m/%Y')}"
