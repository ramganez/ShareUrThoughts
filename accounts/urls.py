
from django.conf.urls import patterns, include, url

from django.views.generic.base import TemplateView
from accounts.views import signup, signin, signout, HomeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ShareUrThoughts.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomeView.as_view(template_name='base.html'), name='home'),

    url(r'^signin/$', signin, name='signin'),
    url(r'^signout/$', signout, name='signout'),

    url(r'^signup/$', signup, name='signup'),


)
