from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from posts.views import (user_posts, PostsList, CreatePost,
                          post_detail)



urlpatterns = patterns('',
    # url(r'^(?P<username>\w+)/$', TemplateView.as_view(template_name='posts/user_posts.html'), name='user_posts'),
    # url(r'^(?P<username>\w+)/$', user_posts, name='user_posts'),

    url(r'^(?P<username>\w+)/$', PostsList.as_view(), name='user_posts'),
    url(r'^(?P<username>\w+)/create$', CreatePost.as_view(), name='create_post'),
    url(r'^(?P<slug>[-\w]+)/$', post_detail, name='post_detail'),
)
