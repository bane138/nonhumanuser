from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Blog(models.Model):
	name = models.CharField(max_length=250)
	tagline = models.TextField()

	def __str__(self):
		return self.name

class Entry(models.Model):
	blog = models.ForeignKey(Blog)	
	title = models.CharField(max_length=250)
	body = models.TextField()
	slug = models.SlugField(editable=False)
	description = models.TextField(blank=True, null=True)
	active =  models.BooleanField(default=False)
	publish_date = models.DateTimeField('published date')
	modified_date = models.DateTimeField()
	category = models.ForeignKey('Category', 
		on_delete=models.PROTECT, 
		blank=True, 
		null=True)
	number_comments = models.IntegerField(default=0)

	def save(self):
		if not self.id:
			self.slug = slugify(self.title)

		super(Entry, self).save()

	def __str__(self):
		return self.title

class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	created = models.DateTimeField('created date')
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name