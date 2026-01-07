from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Servico(models.Model):
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = "Serviços"
        ordering = ['id', 'titulo']

    titulo = models.CharField(max_length=150)
    descricao = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)

    icone = models.CharField(
        max_length=50,
        help_text="Ex: fa-file-invoice, fa-balance-scale, fa-comments",
    )
    # banner = models.ImageField(upload_to = 'cursos_livres/media/banner/', null=True)
    ordem = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)


    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    dt_alteracao = models.DateField(auto_now=True)

    user_inclusao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ServicoUserInclusao')
    user_ultima_alteracao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ServicoUserAlteracao', null=True, blank=True)

    def __str__(self):
        return '%s' % (self.titulo)


class Noticia(models.Model):
    class Meta:
        verbose_name = 'Notícia_Legado'
        verbose_name_plural = "Notícias_Legado"
        ordering = ['id', 'titulo']

         
    titulo = models.CharField(max_length=150)
    # banner_pequeno = models.ImageField()    
    # banner_carroussel = models.ImageField()    
    corpo_da_noticia = models.TextField()
    

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class NoticiasFazenda(models.Model):
    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = "Notícias"
        ordering = ['-dt_inclusao', '-id']  # Mais recente primeiro
        
    # Informações Básicas
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título principal da notícia (máx. 200 caracteres)"
    )
    
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name="URL amigável",
        help_text="Gerado automaticamente a partir do título"
    )
    
    resumo = models.CharField(
        max_length=300,
        verbose_name="Resumo/Descrição",
        help_text="Breve descrição que aparece no carrossel e cards (máx. 300 caracteres)"
    )
    
    # Imagens
    banner_pequeno = models.ImageField(
        upload_to='noticias/thumbnails/%Y/%m/',
        verbose_name="Banner Pequeno (Card)",
        help_text="Imagem para cards de notícias (recomendado: 400x300px)"
    )
    
    banner_carrossel = models.ImageField(
        upload_to='noticias/banners/%Y/%m/',
        verbose_name="Banner Carrossel",
        help_text="Imagem para o carrossel principal (recomendado: 1200x400px)"
    )
    
    # Conteúdo
    corpo_da_noticia = models.TextField(
        verbose_name="Corpo da Notícia",
        help_text="Conteúdo completo da notícia"
    )
    
    links_uteis = models.TextField(
        blank=True,
        null=True,
        verbose_name="Links Úteis",
        help_text="Links relacionados (um por linha ou formato JSON)"
    )
    
    # Metadados
    autor = models.CharField(
        max_length=100,
        default="Secretaria da Fazenda",
        verbose_name="Autor",
        help_text="Nome do autor ou órgão responsável"
    )
    
    # categoria = models.CharField(
    #     max_length=50,
    #     choices=[
    #         ('tributacao', 'Tributação'),
    #         ('servicos', 'Serviços'),
    #         ('legislacao', 'Legislação'),
    #         ('eventos', 'Eventos'),
    #         ('comunicados', 'Comunicados'),
    #         ('outros', 'Outros'),
    #     ],
    #     default='comunicados',
    #     verbose_name="Categoria"
    # )
    
    # Datas
    dt_inclusao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
  
    dt_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    # Controles de Visibilidade
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Desmarque para ocultar a notícia do site"
    )
    
    destaque = models.BooleanField(
        default=False,
        verbose_name="Destaque",
        help_text="Marque para exibir esta notícia no carrossel principal"
    )

    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta Description",
        help_text="Descrição para motores de busca (máx. 160 caracteres)"
    )
    
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Meta Keywords",
        help_text="Palavras-chave separadas por vírgula"
    )
    
    # Estatísticas
    visualizacoes = models.PositiveIntegerField(
        default=0,
        verbose_name="Visualizações",
        editable=False
    )
    
    def save(self, *args, **kwargs):
        """Gera slug automaticamente se não existir"""
        if not self.slug:
            self.slug = slugify(self.titulo)
            # Garante unicidade do slug
            original_slug = self.slug
            counter = 1
            while Noticia.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Gera meta_description a partir do resumo se não fornecida
        if not self.meta_description and self.resumo:
            self.meta_description = self.resumo[:160]
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Retorna a URL da notícia"""
        return reverse('noticia_detalhe', kwargs={'slug': self.slug})
    
    def incrementar_visualizacoes(self):
        """Incrementa contador de visualizações"""
        self.visualizacoes += 1
        self.save(update_fields=['visualizacoes'])
    
    @property
    def esta_recente(self):
        """Verifica se a notícia foi publicada nos últimos 7 dias"""
        dias = (timezone.now() - self.data_publicacao).days
        return dias <= 7
    
    def __str__(self):
        return self.titulo

class PaginasRelacionadas(models.Model):
    titulo = models.CharField(max_length=100, help_text="Aparece ao passar o mouse")
    imagem = models.ImageField(upload_to='paginasrelacionadas/')
    link = models.URLField()

    def __str__(self):
        return self.titulo


class AcessoRapido(models.Model):
    titulo = models.CharField(max_length=100)
    link = models.URLField()
    icone = models.CharField(
        max_length=50,
        help_text="Coloque aqui o nome da classe do ícone FontAwesome. Ex: 'fa-solid fa-book-open'"
    )

    def __str__(self):
        return self.titulo

from django.db import models


class SiteConfiguracao(models.Model):
    nome_site = models.CharField(
        max_length=150,
        default="Prefeitura de Nova Friburgo"
    )

    telefone = models.CharField(
        "Telefone",
        max_length=30,
        blank=True,
        null=True
    )

    whatsapp = models.CharField(
        "WhatsApp",
        max_length=30,
        blank=True,
        null=True,
        help_text="Ex: 5522999999999 (somente números)"
    )

    email = models.EmailField(
        "E-mail institucional",
        blank=True,
        null=True
    )

    endereco = models.TextField(
        "Endereço completo com horário de funcionamento",
        blank=True,
        null=True
    )

    link_instagram = models.URLField(
        "Instagram",
        blank=True,
        null=True
    )

    link_facebook = models.URLField(
        "Facebook",
        blank=True,
        null=True
    )

    link_youtube = models.URLField(
        "YouTube",
        blank=True,
        null=True
    )

    link_site = models.URLField(
        "Website oficial",
        blank=True,
        null=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        self.pk = 1  # Força sempre ser o ID = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Configurações do Site (Registro Único)"

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configuração do Site"


class LinkRodape(models.Model):

    
    TIPO_CHOICES = (
        ('PLATAFORMA', 'Plataforma'),
        ('SISTEMA', 'Sistema'),
    )

    titulo = models.CharField(max_length=100)

    url = models.URLField(
        "Link de redirecionamento",
        help_text="Ex: https://seusite.com.br/pagina"
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='SISTEMA'
    )
    ordem = models.PositiveIntegerField(default=0)

    abrir_em_nova_aba = models.BooleanField(
        "Abrir em nova aba?",
        default=False
    )
    

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ordem"]
        verbose_name = "Link do rodapé"
        verbose_name_plural = "Links do rodapé"

    def __str__(self):
        return self.titulo
