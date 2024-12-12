from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Cliente


class ClienteCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}),
        help_text="A senha deve ter pelo menos 8 caracteres.",
    )
    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'}),
        help_text="Digite a mesma senha para confirmação.",
    )

    class Meta:
        model = Cliente
        fields = ['username', 'email', 'cpf', 'data_nascimento', 'endereco']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'data_nascimento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Data de nascimento'}
            ),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite seu endereço', 'rows': 3}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ClienteAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
        label="Usuário",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label="Senha",
    )
