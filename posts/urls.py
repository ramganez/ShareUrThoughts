from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from posts.views import (PostsList, CreatePost, UpdatePost,
                         DeletePost, post_detail, create_comments)



urlpatterns = patterns('',
    # url(r'^(?P<username>\w+)/$', TemplateView.as_view(template_name='posts/user_posts.html'), name='user_posts'),
    # url(r'^(?P<username>\w+)/$', user_posts, name='user_posts'),

    # username Matches alphanumeric and spl char(-._+@)

    url(r'^(?P<username>[\w.@+-]+)/$', PostsList.as_view(), name='user_posts'),
    url(r'^(?P<username>\w+)/create$', CreatePost.as_view(), name='create_post'),
    url(r'^(?P<username>\w+)/update/(?P<slug>[-\w]+)$', UpdatePost.as_view(), name='update_post'),
    url(r'^(?P<username>\w+)/delete/(?P<slug>[-\w]+)$', DeletePost.as_view(), name='delete_post'),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[-\w]+)/$', post_detail, name='post_detail'),

    #comment
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[-\w]+)/comment$', create_comments, name='create_comment'),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[-\w]+)/reply/(?P<p_id>[0-9]+)$', create_comments, name='create_reply'),


)
