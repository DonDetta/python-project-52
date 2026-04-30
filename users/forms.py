from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'


class CustomUserUpdateForm(CustomUserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(
            username__iexact=username
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                self.instance.unique_error_message(User, ['username'])
            )
        return username
