from django.contrib import admin
from .models import Categoria, Produto, Cliente, Pedido, ItemPedido


# Registro de Categorias
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')  # Exibe os campos no painel
    search_fields = ('nome',)  # Campo de busca
    ordering = ('nome',)  # Ordenação padrão


# Registro de Produtos
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'categoria', 'data_criacao')  # Campos exibidos no painel
    list_filter = ('categoria', 'data_criacao')  # Filtros laterais
    search_fields = ('nome', 'descricao')  # Campo de busca
    list_editable = ('preco',)  # Permite editar o preço diretamente na lista
    ordering = ('-data_criacao',)  # Ordena por data de criação (mais recente primeiro)
    date_hierarchy = 'data_criacao'  # Navegação por datas


# Registro de Clientes
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'cpf', 'is_staff', 'is_active', 'date_joined')  # Campos exibidos
    search_fields = ('username', 'email', 'cpf')  # Campo de busca
    list_filter = ('is_staff', 'is_active', 'date_joined')  # Filtros laterais
    ordering = ('username',)  # Ordenação padrão
    readonly_fields = ('date_joined', 'last_login')  # Campos apenas leitura


# Inline para Itens do Pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1  # Número de linhas extras para adicionar
    fields = ('produto', 'quantidade', 'preco_unitario', 'subtotal')  # Campos exibidos
    readonly_fields = ('subtotal',)  # Torna o subtotal apenas leitura


# Registro de Pedidos
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_pedido', 'total', 'status')  # Inclui o campo status
    list_filter = ('status', 'data_pedido')  # Filtra pedidos por status
    search_fields = ('cliente__username', 'id')  # Busca por cliente e ID do pedido
    ordering = ('-data_pedido',)  # Ordena pelo pedido mais recente
    date_hierarchy = 'data_pedido'  # Navegação por data do pedido
    readonly_fields = ('total',)  # Total apenas leitura
    inlines = [ItemPedidoInline]  # Adiciona os itens do pedido diretamente no formulário


# Registro de Itens do Pedido
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'produto', 'quantidade', 'preco_unitario', 'subtotal')  # Campos exibidos no painel
    search_fields = ('produto__nome', 'pedido__id')  # Busca por produto e pedido
    ordering = ('pedido',)  # Ordena por pedido
    readonly_fields = ('subtotal',)  # Subtotal apenas leitura
