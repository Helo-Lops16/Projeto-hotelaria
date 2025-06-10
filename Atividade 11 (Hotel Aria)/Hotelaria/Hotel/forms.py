from django import forms
from .models import quarto
from datetime import date

class quartoForms(forms.ModelForm):
    status_escolha = [
        (True, 'Disponível'),
        (False, 'Reservado'),
    ]

    status = forms.ChoiceField(choices=status_escolha, widget=forms.Select())
    data_reserva = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': date.today().isoformat()
            }
        ),
        required=False
    )

    class Meta:
        model = quarto
        fields = [
            'num_Quarto', 'qtd_Hospedes', 'estilo', 'tipo', 
            'valor', 'descricao', 'status', 'data_reserva', 'img'
        ]