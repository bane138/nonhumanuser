from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class GameGroup(models.Model):
    name = models.CharField(max_length=255)
    game_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
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


class GameType(models.Model):
    name = models.CharField(max_length=225)
    era = models.ForeignKey('GameEra',
                            on_delete=models.PROTECT,
                            blank=True,
                            null=True,
                            related_name='era')
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)
    created_date = models.DateTimeField('created date')
    modified_date = models.DateTimeField('modified date')
    slug = models.SlugField(blank=True, null=True)

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)

        super(GameType, self).save()

    def __str__(self):
        return self.name


class GameEra(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)

        super(GameEra, self).save()

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey('GameGroup',
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    game_type = models.ForeignKey('GameType',
                                  on_delete= models.PROTECT,
                                  blank=True,
                                  null=True,
                                  related_name='game_type')
    body = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)
    number_views = models.IntegerField(default=0)
    number_comments = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)
    created_date = models.DateTimeField('created date')
    modified_date = models.DateTimeField()
    publish_date = models.DateTimeField(null=True, blank=True, default=None)
    thumbnail = models.ImageField(upload_to='actual_play/image/%Y/%m/%d',\
     blank=True, null=True)
    image = models.ImageField(upload_to='actual_play/image/%Y/%m/%d',\
     blank=True, null=True)
    audio_ogg = models.FileField(upload_to='actual_play/audio/%Y/%m/%d/',\
     blank=True, null=True)
    audio_mp3 = models.FileField(upload_to='actual_play/audio/%Y/%m/%d/',\
     blank=True, null=True)
    video_ogv = models.FileField(upload_to='actual_play/video/%Y/%m/%d/',\
     blank=True, null=True)
    video_mp4 = models.FileField(upload_to='actual_play/video/%Y/%m/%d/',\
     blank=True, null=True)
    audio_url_ogg = models.CharField(max_length=255, blank=True, null=True)
    audio_url_mp3 = models.CharField(max_length=255, blank=True, null=True)
    video_url_ogv = models.CharField(max_length=255, blank=True, null=True)
    video_url_mp4 = models.CharField(max_length=255, blank=True, null=True)

    @property
    def sidebar_icon_class(self):
        return 'sm_icon_class_actual_play'


    def get_group_name(self):
        if self.group:
            group = GameGroup.get(pk=self.group_id)

        return group.slug

    def get_game_type(self):
        if self.game_type:
            game_type = GameType.objects.get(pk=self.game_type_id)

        return game_type.slug

    def get_absolute_url(self):
        return reverse('game', kwargs={'game_type': self.get_game_type(),
            'slug': self.slug})

    def save(self):
        if not self.id:
            self.slug = slugify(self.title)

        super(Game, self).save()

    def __str__(self):
        return self.title


class GameComment(models.Model):
    game = models.ForeignKey(Game, related_name='comments')
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='actual_play_user',
        null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.game.title


class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    group = models.ManyToManyField(GameGroup)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField('created date')
    image = models.ImageField(upload_to='actual_play/player/%Y/%m/%d',\
     blank=True, null=True)


    def __str__(self):
        return self.nickname

