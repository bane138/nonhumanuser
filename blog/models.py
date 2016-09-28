from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone

# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=250)
    tagline = models.TextField()
    created_date = models.DateTimeField('created date')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=250)
    body = models.TextField()
    slug = models.SlugField(editable=False)
    description = models.TextField(null=True, blank=True)
    active =  models.BooleanField(default=False)
    created_date = models.DateTimeField('created date')
    modified_date = models.DateTimeField()
    publish_date = models.DateTimeField(null=True, blank=True, default=None)
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
	blank=True, null=True)
    number_views = models.IntegerField(default=0)
    number_comments = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='entry/%Y/%m/%d', blank=True, null=True)
    image = models.ImageField(upload_to='entry/%Y/%m/%d', blank=True, null=True)

    @property
    def sidebar_icon_class(self):
        if self.category.name == 'Stories':
            return 'sm_icon_class_stories'
        else:
            return 'sm_icon_class_articles'

    def save(self):
        if not self.id:
            self.slug = slugify(self.title)

        super(Entry, self).save()

    def get_category_name(self):
        name = 'blog'
        if self.category:
            category = Category.objects.get(name=self.category)
            if category.name == 'Stories':
                name = 'story'
            else:
                name = category.name.replace('s', '').lower()

        return name

    def get_absolute_url(self):
        return reverse(self.get_category_name(), kwargs={'slug': self.slug})


    def __str__(self):
        return self.title


class EntryComment(models.Model):
    entry = models.ForeignKey(Entry, related_name='comments')
    body = models.TextField()
    author = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField('created date')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
