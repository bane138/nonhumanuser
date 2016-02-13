from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class GameGroup(models.Model):
	name = models.CharField(max_length=255)
	game_type = models.CharField(max_length=255)
	active = models.BooleanField(default=True)
	created_date = models.DateTimeField('created date')
	last_played = models.DateTimeField('last played')
	status = models.CharField(max_length=100)
	slug = models.SlugField(blank=True, null=True)

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		super(GameGroup, self).save()

	def __str__(self):
		return self.name


class Game(models.Model):
	name = models.CharField(max_length=255)
	group = models.ForeignKey('GameGroup', 
		on_delete=models.PROTECT,
		blank=True,
		null=True)
	source_destination = models.CharField(max_length=255)
	description = models.TextField()
	active = models.BooleanField(default=False)
	slug = models.SlugField(blank=True, null=True)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		super(Game, self).save()

	def __str__(self):
		return self.name


class Player(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	nickname = models.CharField(max_length=100)
	email = models.CharField(max_length=255)
	group = models.ManyToManyField(GameGroup)
	active = models.BooleanField(default=True)
	created_date = models.DateTimeField('created date')


	def __str__(self):
		return self.nickname

