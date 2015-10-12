import ipdb

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from accounts.views import LoginRequiredMixin
from posts.models import Post, Comment
from posts.forms import PostForm, CommentForm

# Create your views here.

# views for posts
def user_posts(request, username):
    return render(request, 'posts/user_posts.html', {'user': username})


class PostsList(LoginRequiredMixin, ListView):
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


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/create_and_update.html'

    def form_valid(self, form):
        # ipdb.set_trace()

        form.instance.fk_user = User.objects.get(username=self.kwargs['username'])
        return super(CreatePost, self).form_valid(form)

    def get_success_url(self):
        return reverse('posts:user_posts', kwargs={'username': self.kwargs['username']})


def post_detail(request, pk, slug):
    # ipdb.set_trace()
    post = get_object_or_404(Post, slug=slug)
    node_set = post.comment_set.all()

    return render(request, 'posts/post_detail.html', {'post': post, 'node_set': node_set})

class UpdatePost(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/create_and_update.html'

    def get_object(self):
        # ipdb.set_trace()
        user_obj = User.objects.get(username=self.kwargs['username'])
        obj = Post.objects.get(fk_user__username=user_obj.username, deleted=False, slug=self.kwargs['slug'])
        return obj


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/delete_post.html'

    def get_success_url(self):
        return '/posts/%s' % self.kwargs['username']

    def get_object(self):
        # ipdb.set_trace()
        user_obj = User.objects.get(username=self.kwargs['username'])
        obj = Post.objects.get(fk_user__username=user_obj.username, deleted=False, slug=self.kwargs['slug'])
        return obj

    def delete(self, request, *args, **kwargs):
        # ipdb.set_trace()
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()

        return HttpResponseRedirect(success_url)


# views for comments

@login_required
def create_comment(request, pk, slug):

    post = get_object_or_404(Post, slug=slug)
    node_set = post.comment_set.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            user_obj = request.user
            form.instance.fk_user = user_obj
            try:
                post_obj = Post.objects.get(slug=slug)
                form.instance.fk_post = post_obj
                form.save()
                node_set = post_obj.comment_set.all()
            except ObjectDoesNotExist:
                raise Http404

            return render(request, 'posts/post_detail.html', {'post': post_obj, 'node_set': node_set})

        else:
            form = CommentForm()

    else:
        form = CommentForm()

    return render(request, 'posts/comment_form.html', {'form': form, 'post': post, 'node_set': node_set})


@login_required
def create_thread(request, pk, slug, p_id):

    post = get_object_or_404(Post, slug=slug)
    node_set = post.comment_set.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            user_obj = request.user
            form.instance.fk_user = user_obj
            try:
                post_obj = Post.objects.get(slug=slug)
                form.instance.fk_post = post_obj

                # if threaded case
                form.instance.parent_cmt = Comment.objects.get(id=p_id)
                form.save()

                node_set = post_obj.comment_set.all()
            except ObjectDoesNotExist:
                raise Http404

            return render(request, 'posts/post_detail.html', {'post': post_obj, 'node_set': node_set})
        else:
            form = CommentForm()

    else:
        form = CommentForm()

    return render(request, 'posts/comment_form.html', {'form': form, 'post': post, 'node_set': node_set})
