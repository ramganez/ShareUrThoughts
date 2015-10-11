import ipdb

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Pick a username'}),
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = self.cleaned_data.get('username', None)
        email = self.cleaned_data.get('email', None)

        try:
            user_obj = User.objects.get(username=username)

        except ObjectDoesNotExist:
            user_obj = None

        if user_obj:
            raise forms.ValidationError('username is already taken')

        try:
            user_obj = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user_obj = None

        if user_obj:
            raise forms.ValidationError('email is already taken')

        return cleaned_data


class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect username or password")

        return self.cleaned_data

