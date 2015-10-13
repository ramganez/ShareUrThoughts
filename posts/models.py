from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    fk_user = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField()
    posted_on = models.DateField(default=datetime.now)
    deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.id, 'slug': self.slug})

    def get_update_url(self):
        return reverse('posts:update_post', kwargs={'username': self.fk_user.username, 'slug': self.slug})

    def get_delete_url(self):
        return reverse('posts:delete_post', kwargs={'username': self.fk_user.username, 'slug': self.slug})


class Comment(MPTTModel):
    fk_user = models.ForeignKey(User)
    fk_post = models.ForeignKey(Post)
    comment = models.TextField(max_length=255)
    parent_cmt = TreeForeignKey('self', null=True, blank=True, related_name='child_cmt', db_index=True)
    commented_on = models.DateField(default=datetime.now)
    deleted = models.BooleanField(default=False)

    class MPTTMeta:
        parent_attr = 'parent_cmt'
        order_insertion_by = ['commented_on']

    def __unicode__(self):
        return '%s - comment' % self.fk_user


