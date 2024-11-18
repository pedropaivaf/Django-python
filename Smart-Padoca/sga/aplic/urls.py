from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Rota para exibir o index.html
]
