import ipdb

from django.shortcuts import render

# Create your views here.

def user_posts(request, username):

	return render(request, 'posts/user_posts.html', {'user':username})

