from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class WaitlistForm(forms.Form):
    target_price = forms.DecimalField(
        label="Желаемая цена в баксах",
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "step": "0.01",
            "placeholder": "Пример: 9.99"
        })
    )