from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

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
	title = models.CharField(max_length=255)
	group = models.ForeignKey('GameGroup', 
		on_delete=models.PROTECT,
		blank=True,
		null=True)
	description = models.TextField()
	active = models.BooleanField(default=False)
	number_views = models.IntegerField(default=0)
	number_comments = models.IntegerField(default=0)
	slug = models.SlugField(blank=True, null=True)
	created_date = models.DateTimeField('created date')
	modified_date = models.DateTimeField()
	publish_date = models.DateTimeField(null=True, blank=True, default=None)
	image = models.ImageField(upload_to='actual_play/image/%Y/%m/%d', blank=True, null=True)
	audio_ogg = models.FileField(upload_to='actual_play/audio/%Y/%m/%d/', blank=True, null=True)
	audio_mp3 = models.FileField(upload_to='actual_play/audio/%Y/%m/%d/', blank=True, null=True)
	video_ogg = models.FileField(upload_to='actual_play/video/%Y/%m/%d/', blank=True, null=True)
	video_mp4 = models.FileField(upload_to='actual_play/video/%Y/%m/%d/', blank=True, null=True)

	def save(self):
		if not self.id:
			self.slug = slugify(self.title)

		super(Game, self).save()

	def __str__(self):
		return self.title


class GameComment(models.Model):
	game = models.ForeignKey(Game, related_name='comments')
	body = models.TextField()
	author = models.CharField(max_length=200)
	created_date = models.DateTimeField(auto_now=True)
	approved = models.BooleanField(default=False)

	def approve(self):
		self.approved = True
		self.save()

	def __str__(self):
		return self.text


class Player(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	nickname = models.CharField(max_length=100)
	email = models.CharField(max_length=255)
	group = models.ManyToManyField(GameGroup)
	active = models.BooleanField(default=True)
	created_date = models.DateTimeField('created date')
	image = models.ImageField(upload_to='actual_play/player/%Y/%m/%d', blank=True, null=True)


	def __str__(self):
		return self.nickname

