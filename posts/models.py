import itertools

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


# Create your models here.


class Post(models.Model):
    fk_user = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField()
    posted_on = models.DateField(default=datetime.now)
    deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.id, 'slug': self.slug})

    def get_update_url(self):
        return reverse('posts:update_post', kwargs={'username': self.fk_user.username, 'slug': self.slug})

    def get_delete_url(self):
        return reverse('posts:delete_post', kwargs={'username': self.fk_user.username, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def save(self):
        post_obj = super(Post, self).save(commit=False)

        after_slugify = slugify(post_obj.title)

        for i in itertools.count(1):
            if not Post.objects.filter(slug=after_slugify).exists():
                break
            after_slugify.slug = '%s-%d' % (after_slugify, i)

        post_obj.save()

        return post_obj



class Comment(models.Model):
    fk_user = models.ForeignKey(User)
    fk_post = models.ForeignKey(Post)
    comment = models.TextField()
    commented_on = models.DateField(default=datetime.now)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - comment' % self.fk_user



