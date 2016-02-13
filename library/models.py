from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Stack(models.Model):
	name = models.CharField(max_length=250)
	tagline = models.TextField()
	active = models.BooleanField(default=False)
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
	source_destination = models.CharField(max_length=255)
	description = models.TextField()
	stack = models.ForeignKey('Stack', 
		on_delete=models.PROTECT, 
		blank=True,
		null=True)
	active = models.BooleanField(default=False)
	slug = models.SlugField(blank=True, null=True)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		super(Item, self).save()

	def __str__(self):
		return self.name

class ItemType(models.Model):
	name = models.CharField(max_length=100)
	active = models.BooleanField(default=False)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()

	def __str__(self):
		return self.name

