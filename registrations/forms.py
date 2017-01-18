from django import forms
from .models import TempUserProfile, UserProfile
from django.contrib.auth.models import User


class FirstForm(forms.ModelForm):
    class Meta:
        model = TempUserProfile
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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class ProfileAddForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['job', 'education', 'description', 'avatar', 'date_of_birth']
        widgets = {
            'job': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job'}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Education'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of birth'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

#    def clean_avatar(self):
#        avatar = self.cleaned_data.get('avatar')
#        if avatar is None:
#            raise forms.ValidationError(u'Добавьте картинку')
 #       if 'image' not in avatar.content_type:
 #           raise forms.ValidationError(u'Неверный формат картинки')
#        return avatar


