from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

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
	description = models.TextField(blank=True, null=True)
	active =  models.BooleanField(default=False)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()
	category = models.ForeignKey('Category', 
		on_delete=models.PROTECT, 
		blank=True, 
		null=True)
	number_comments = models.IntegerField(default=0)
	image = models.ImageField(upload_to='entry/%Y/%m/%d', blank=True, null=True)

	def save(self):
		if not self.id:
			self.slug = slugify(self.title)

		super(Entry, self).save()

	def get_category_name(self):
		name = 'blog'
		if self.category:
			category = Category.objects.get(pk=self.category)
			name = category.name

		return name

	def get_absolute_url(self):
		return reverse(self.get_category_name(), kwargs={'slug': self.slug})


	def __str__(self):
		return self.title

class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField('created date')
	active = models.BooleanField(default=False)

	def __str__(self):
		return self.name