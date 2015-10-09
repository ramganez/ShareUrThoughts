import ipdb

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from accounts.views import LoginRequiredMixin
from posts.models import Post, Comment
from posts.forms import PostForm

# Create your views here.


def user_posts(request, username):
    return render(request, 'posts/user_posts.html', {'user': username})


class PostsList(ListView):
    template_name = 'posts/user_posts.html'

    def get_queryset(self):
        # ipdb.set_trace()
        user_obj = User.objects.get(username=self.kwargs['username'])
        qs = Post.objects.filter(fk_user__username=user_obj.username, deleted=False)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PostsList, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.kwargs['username'])
        return context


class CreatePost(CreateView):
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        # ipdb.set_trace()
        form.instance.fk_user = User.objects.get(username=self.kwargs['username'])
        return super(CreatePost, self).form_valid(form)


def post_detail(request, slug):
    # ipdb.set_trace()
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'posts/post_detail.html', {'post': post})





