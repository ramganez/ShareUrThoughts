from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from accounts.forms import SignUpForm, SigninForm

# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'signup_form': form})


def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                return redirect('posts:user_posts', username=username)
            else:
                form = SigninForm()
    else:
        form = SigninForm()
    return render(request, 'accounts/signup.html', {'signup_form': form})


def signout(request):
    pass

