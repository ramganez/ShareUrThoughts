import ipdb

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from accounts.forms import SignUpForm, SigninForm
from posts.models import Post

# Create your views here.


class LoginRequiredMixin(object):

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class HomeView(ListView):
    model = Post
    template_name = 'base.html'

    def get_queryset(self):
        posts = Post.objects.filter(deleted=False)
        return posts


def signup(request):
    if request.method == 'POST':
        # ipdb.set_trace()
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('posts:user_posts', username=username)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup_in.html', {'signup_in_form': form})


def signin(request):
    # ipdb.set_trace()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    return redirect('posts:user_posts', username=username)
            else:
                form = SigninForm()
    else:
        form = SigninForm()
    return render(request, 'accounts/signup_in.html', {'signup_in_form': form})


def signout(request):
    logout(request)
    return redirect('home')


