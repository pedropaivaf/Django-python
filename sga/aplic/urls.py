from django.urls import path
from .views import (
    IndexView,
    listar_produtos,
    registro_login,
    sair,
    carrinho,
    adicionar_ao_carrinho,
    remover_do_carrinho,
    finalizar_compra,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Página principal usando IndexView
    path('produtos/', listar_produtos, name='produtos'),  # Página de listagem de produtos
    path('login/', registro_login, name='login'),  # Página de login e cadastro
    path('logout/', sair, name='logout'),  # Logout
    path('carrinho/', carrinho, name='carrinho'),  # Página do carrinho
    path('carrinho/adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),  # Adicionar ao carrinho
    path('carrinho/remover/<int:item_id>/', remover_do_carrinho, name='remover_do_carrinho'),  # Remover do carrinho
    path('carrinho/finalizar/', finalizar_compra, name='finalizar_compra'),  # Finalizar compra
]
