from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone

# Create your models here.
class Stack(models.Model):
	name = models.CharField(max_length=250)
	tagline = models.TextField()
	active = models.BooleanField(default=True)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()
	slug = models.SlugField(blank=True, null=True)

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		super(Stack, self).save()

	def __str__(self):
		return self.name


class Item(models.Model):
	item_type = models.ForeignKey('ItemType', 
		on_delete=models.PROTECT, 
		blank=True,
		null=True)
	title = models.CharField(max_length=250)
	body = models.TextField()
	slug = models.SlugField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	active =  models.BooleanField(default=False)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()
	publish_date = models.DateTimeField(null=True, blank=True, default=None)
	stack = models.ForeignKey('Stack', 
		on_delete=models.PROTECT, 
		blank=True,
		null=True)
	number_views = models.IntegerField(default=0)
	number_comments = models.IntegerField(default=0)
	thumbnail = models.ImageField(upload_to='library/item/%Y/%m/%d', blank=True, null=True)
	image = models.ImageField(upload_to='library/item/%Y/%m/%d', blank=True, null=True)
	resource = models.FileField(upload_to='library/item/%Y/%m/%d', blank=True, null=True)

	def save(self):
		if not self.id:
			self.slug = slugify(self.title)

		super(Item, self).save()

	def get_stack_name(self):
		name = 'resources'
		if self.stack:
			stack = Stack.objects.get(pk=self.stack_id)
			#name = stack.name.replace('s', '').lower()

		return stack.name

	def get_absolute_url(self):
		return reverse('item', kwargs={'stack': self.get_stack_name(), 'slug': self.slug})

	def __str__(self):
		return self.title


class ItemComment(models.Model):
	comment = models.ForeignKey(Item, related_name='comments')
	body = models.TextField()
	author = models.CharField(max_length=200)
	created_date = models.DateTimeField(auto_now=True)
	approved = models.BooleanField(default=False)

	def approve(self):
		self.approved = True
		self.save()

	def __str__(self):
		return self.text


class ItemType(models.Model):
	name = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()

	def __str__(self):
		return self.name

