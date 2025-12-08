from django.db import models


class Ferramenta(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    link = models.URLField(max_length=500)
    keywords = models.TextField(
        blank=True,
        help_text="Separe as palavras-chave por ponto e vírgula (;)"
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ferramenta / Sistema"
        verbose_name_plural = "Ferramentas / Sistemas"
        ordering = ['titulo']

    def lista_keywords(self):
        if not self.keywords:
            return []
        return [k.strip().lower() for k in self.keywords.split(";") if k.strip()]
    @property
    
    def link_curto(self):
        return self.link[:50]+"..."

    def __str__(self):
        return self.titulo
