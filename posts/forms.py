import ipdb
import itertools
from django.template.defaultfilters import slugify

from posts.models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text']

    def save(self):
        instance = super(PostForm, self).save(commit=False)

        orig = slugify(instance.title)
        instance.slug = orig

        for x in itertools.count(1):
            if not Post.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)

        instance.save()

        return instance


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1,'cols': 50}),
        }
