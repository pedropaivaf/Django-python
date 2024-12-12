from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Produto, Categoria, Cliente, Pedido, ItemPedido
from .forms import ClienteCreationForm


# Página principal
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.order_by('-data_criacao')[:10]  # Ordena por data de criação
        return context


# Página de Produtos
class ProdutosView(ListView):
    model = Produto
    template_name = 'produtos.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Todas as categorias
        categoria_selecionada = self.request.GET.get('categoria')
        context['categoria_selecionada'] = categoria_selecionada  # Define a categoria selecionada
        return context

    def get_queryset(self):
        queryset = Produto.objects.all()
        categoria_id = self.request.GET.get('categoria')  # Obtém o ID da categoria da query string
        if categoria_id:  # Se houver uma categoria selecionada
            queryset = queryset.filter(categoria__id=categoria_id)
        return queryset


def listar_produtos(request):
    categorias = Categoria.objects.all()
    categoria_selecionada = request.GET.get('categoria')  # Obter categoria selecionada
    if categoria_selecionada:
        produtos = Produto.objects.filter(categoria__id=categoria_selecionada)
    else:
        produtos = Produto.objects.all()

    return render(request, 'produtos.html', {
        'categorias': categorias,
        'produtos': produtos,
        'categoria_selecionada': categoria_selecionada
    })


@login_required(login_url='/login/')  # Redireciona para a página de login
def carrinho(request):
    pedido = Pedido.objects.filter(cliente=request.user, status='A').first()
    itens = pedido.itens.all() if pedido else []
    total = sum(item.subtotal for item in itens) if itens else 0

    if not itens:
        messages.info(request, "Seu carrinho está vazio.")

    return render(request, 'carrinho.html', {'pedido': pedido, 'itens': itens, 'total': total})


@login_required(login_url='/login/')  # Redireciona para a página de login
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    pedido, created = Pedido.objects.get_or_create(cliente=request.user, status='A')

    # Obtém a quantidade enviada no formulário, padrão é 1
    quantidade = int(request.POST.get('quantidade', 1))

    # Procura o item no pedido ou cria um novo
    item, item_created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)
    if not item_created:
        # Atualiza a quantidade do item existente
        item.quantidade += quantidade
    else:
        # Define a quantidade para um novo item
        item.quantidade = quantidade

    # Atualiza o subtotal e salva o item
    item.preco_unitario = produto.preco
    item.subtotal = item.quantidade * item.preco_unitario
    item.save()

    # Recalcula o total do pedido
    pedido.calcular_total()

    messages.success(request, f"{quantidade} unidade(s) de {produto.nome} foram adicionadas ao carrinho.")
    return redirect('produtos')


@login_required(login_url='/login/')  # Redireciona para a página de login
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id, pedido__cliente=request.user, pedido__status='A')
    if item:
        pedido = item.pedido
        item.delete()
        pedido.calcular_total()
        messages.success(request, "Item removido do carrinho.")
    else:
        messages.error(request, "O item não existe ou já foi removido.")
    return redirect('carrinho')


@login_required(login_url='/login/')  # Redireciona para a página de login
def finalizar_compra(request):
    pedido = Pedido.objects.filter(cliente=request.user, status='A').first()
    if pedido:
        pedido.status = 'F'
        pedido.save()
        messages.success(request, "Pedido enviado com sucesso! Obrigado por comprar conosco.")
    else:
        messages.error(request, "Não há nenhum pedido aberto para finalizar.")
    return redirect('index')  # Redireciona para a página principal


# Login e Cadastro Unificado
def registro_login(request):
    form = ClienteCreationForm()  # Inicializa o formulário sempre

    if request.GET.get('next'):
        messages.warning(request, "Você precisa estar logado para acessar esta página.")

    if request.method == 'POST':
        # Verificar se é login
        if 'username_login' in request.POST:
            username = request.POST.get('username_login')
            senha = request.POST.get('senha_login')
            user = authenticate(request, username=username, password=senha)
            if user:
                login(request, user)
                messages.success(request, f"Bem-vindo(a), {user.username}! Login realizado com sucesso.")
                return redirect(request.GET.get('next', 'index'))  # Redirecionar para a página desejada
            else:
                messages.error(request, "Usuário ou senha inválidos. Tente novamente.")
                return redirect('login')

        # Verificar se é cadastro
        elif 'username' in request.POST:
            form = ClienteCreationForm(request.POST)  # Recria o formulário com os dados POST
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Cadastro realizado com sucesso! Você está logado.")
                return redirect('index')  # Redirecionar para a página inicial após cadastro
            else:
                # Enviar mensagens de erro para o template
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

    return render(request, 'login_cadastro.html', {'form': form})


# Logout
@login_required
def sair(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso.")
    return redirect('index')
