from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']  # Ordena as categorias por nome


class Produto(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Produto")
    descricao = models.TextField(verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, verbose_name="Categoria", related_name="produtos"
    )
    imagem = models.ImageField(
        upload_to='produtos/',  # Salva as imagens em uma subpasta chamada "produtos"
        null=True,
        blank=True,
        verbose_name="Imagem do Produto"
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']  # Ordena os produtos por nome


class Cliente(AbstractUser):
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato XXX.XXX.XXX-XX',
            )
        ],
        verbose_name="CPF"
    )
    endereco = models.TextField(blank=True, verbose_name="Endereço")
    data_nascimento = models.DateField(default=timezone.now, verbose_name="Data de Nascimento")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['username']  # Ordena os clientes por nome de usuário


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('A', 'Aberto'),
        ('F', 'Finalizado'),
        ('C', 'Cancelado'),
    ]
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, verbose_name="Cliente", related_name="pedidos"
    )
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", default=0.00)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='A', verbose_name="Status"
    )
    produtos = models.ManyToManyField(
        'Produto', through='ItemPedido', verbose_name="Produtos", related_name="pedidos"
    )

    def calcular_total(self):
        """Calcula o total do pedido com base nos itens do pedido."""
        self.total = sum(item.subtotal for item in self.itens.all())
        self.save()

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente.username}'

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido']  # Ordena os pedidos do mais recente para o mais antigo


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, verbose_name="Pedido", related_name="itens"
    )
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, verbose_name="Produto", related_name="itens_pedido"
    )
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade", default=1)
    preco_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço Unitário", default=0.00
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Subtotal", editable=False, default=0.00
    )

    def save(self, *args, **kwargs):
        """Atualiza o subtotal automaticamente com base na quantidade e preço unitário."""
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} - Pedido {self.pedido.id}'

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
        ordering = ['pedido']  # Ordena os itens por pedido
