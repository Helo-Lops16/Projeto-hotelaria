from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Homepage, name='homepage'),
    path('login', views.Login, name='login'),
    path('logout', views.Sair, name='logout'),
    path('addQuarto', views.addQuarto, name="addQuarto"),
    path('quartos', views.verQuartos, name="quartos"),
    path('reservas', views.reservas, name="reservas"),
    path('removerQuarto', views.removerQuarto, name="removerQuarto"),
    path('reservar-quarto/', views.alt_status, name='reservar_quarto'),
    path('reservas/excluir-antigas/', views.excluir_reservas_antigas, name='excluir_reservas_antigas'),
    path('cancelar-reserva/', views.cancelar_reserva, name='cancelar_reserva'),
    path('addColaborador', views.add_colaborador, name='addColaborador')
]