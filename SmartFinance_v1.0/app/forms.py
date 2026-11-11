from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile 

#форма регістраціі
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Введіть email'})
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


    # Перевірка унікальности email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує")
        return email


    # Зберігаємо коирстувача в базу
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # email як username
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 
    
# Форма редагуваня профиля
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'avatar', 'language', 'theme', 'currency']

