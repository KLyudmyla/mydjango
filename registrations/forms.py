from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class FirstForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['activation_key', 'key_expires']
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Set password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        }
    def clean_email(self):
        """
        clean email field
        """
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Такой адрес электронной почты уже зарегестрирован.')
