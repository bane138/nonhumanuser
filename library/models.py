from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

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
	name = models.CharField(max_length=250)
	description = models.TextField()
	stack = models.ForeignKey('Stack', 
		on_delete=models.PROTECT, 
		blank=True,
		null=True)
	active = models.BooleanField(default=True)
	slug = models.SlugField(blank=True, null=True)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()
	resource = models.FileField(upload_to='library/item/%Y/%m/%d', blank=True, null=True)

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		super(Item, self).save()

	def get_stack_name(self):
		name = 'resources'
		if self.stack:
			stack = Stack.objects.get(pk=self.stack)
			name = stack.name

		return name

	def get_absolute_url(self):
		return reverse(self.get_stack_name(), kwargs={'slug': self.slug})

	def __str__(self):
		return self.name

class ItemType(models.Model):
	name = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()

	def __str__(self):
		return self.name

