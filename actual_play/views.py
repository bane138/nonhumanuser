from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from actual_play.models import GameGroup, Game, GameType
from actual_play.forms import GameCommentForm
from nonhumanuser.utils import *
from nonhumanuser import settings
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from actual_play.models import GameComment
import mimetypes
import datetime
import os

# Create your views here.
class IndexView(View):
        template_name = 'actual_play/index.html'

        def get(self, request, *args, **kwargs):
                context = {}
                game_types = GameType.objects.filter(active=True)
                items_recent = Game.objects.filter(active=True,
                                                                                   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
                items_popular = Game.objects.filter(active=True,
                                                                                   publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
                links = get_main_links()
                context['section'] = {'name': 'Actual Play'}
                context['og_type'] = 'webpage'
                context['og_url'] = 'http://www.nonhumanuser.com/actual_play/'
                context['og_title'] = 'Actual Plays'
                context['og_description'] = 'Call of Cthulhu and Delta Green play sessions'
                context['og_image'] = 'http://www.nonhumanuser.com/images/Actual_Play.png'
                context['game_types'] = game_types
                context['items_recent'] = items_recent
                context['items_popular'] = items_popular
                context['links'] = links
                return render(request, self.template_name, context)


class GameTypeView(View):
        template = 'actual_play/games.html'

        def get(self, request, *args, **kwargs):
                if GameType.objects.filter(slug=self.kwargs['game_type']).exists():
                        game_type = GameType.objects.filter(slug=self.kwargs['game_type']).first()
                        games = Game.objects.filter(game_type=game_type.pk, active=True,
                                publish_date__lte=datetime.datetime.now()).order_by('-publish_date')[0:5]
                else:
                        game_type = GameGroup.objects.filter(slug=self.kwargs['game_type']).first()
                        games = Game.objects.filter(group=game_type.pk, active=True,
                                publish_date__lte=datetime.datetime.now()).order_by('-publish_date')[0:5]
                games_total = Game.objects.all() #
                items_recent = Game.objects.filter(group=game_type.pk, active=True, publish_date__lte=datetime.datetime.now())\
                .order_by('-created_date')[0:5]
                items_popular = Game.objects.filter(group=game_type.pk, active=True, publish_date__lte=datetime.datetime.now())\
                .order_by('-number_comments')[0:5]
                links = get_main_links()
                context = {}

                context['section'] = {'name': 'Actual Play'}
                context['og_type'] = 'webpage'
                context['og_url'] = 'http://www.nonhumanuser.com/actual_play/' + game_type.slug + '/'
                context['og_title'] = game_type.name
                context['og_description'] = game_type.description
                context['og_image'] = ''
                context['game_type'] = game_type
                context['game_type_slug'] = game_type.slug
                context['games'] = games
                context['items_recent'] = items_recent
                context['items_popular'] = items_popular
                context['links'] = links
                context['count'] = games_total.count()
                context['icon_class'] = 'lg_icon_class_actual_play'

                return render(request, self.template, context)


class GameView(View):
        template = 'actual_play/game.html'

        def get(self, request, *args, **kwargs):
                if GameType.objects.filter(slug=self.kwargs['game_type']).exists():
                        game_type = GameType.objects.filter(slug=self.kwargs['game_type']).first()
                        game = Game.objects.filter(slug=self.kwargs['slug'],
                                game_type=game_type.pk).first()
                else:
                        game_type = GameGroup.objects.filter(slug=self.kwargs['game_type']).first()
                        game = Game.objects.filter(slug=self.kwargs['slug'],
                                group=game_type.pk).first()


                items_recent = Game.objects.filter(active=True,
                                                                                   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
                items_popular = Game.objects.filter(active=True,
                                                                                        publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]

                links = get_main_links()
                form = GameCommentForm(request.POST)

                if game:
                        game_type = game.game_type
                        game_comments = game.comments.all()
                        game.number_comments = game_comments.count()
                        game.number_views = game.number_views + 1
                        game.save()
                        context ={
                                'section': {'name': 'Actual Play'},
                                'og_type': 'webpage',
                                'og_url': 'http://www.nonhumanuser.com/actual_play/' + game_type.slug + '/' + game.slug,
                                'og_title': game.title,
                                'og_description': game.description,
                                'og_image': 'http://www.nonhumanuser.com' + game.image.url if game.image else '',
                                'game': game,
                                'game_type': game_type,
                                'game_type_slug': game_type.slug,
                                'items_recent': items_recent,
                                'items_popular': items_popular,
                                'links': links,
                                'form': form,
                                'comments': None,  # game_comments
                                'icon_class': 'lg_icon_class_actual_play',
                        }
                else:
                        context = {
                                'section': {'name': 'Actual Play'},
                                'og_type': 'webpage',
                                'og_url': 'http://www.nonhumanuser.com/actual_play/' + self.kwargs['game_type'] + '/' + \
                                                  self.kwargs['slug'],
                                'og_title': 'No game available',
                                'og_description': 'No game available',
                                'og_image': 'http://www.nonhumanuser.com',
                                'game': game,
                                'game_type': game_type,
                                'game_type_slug': game_type.slug,
                                'items_recent': items_recent,
                                'items_popular': items_popular,
                                'links': links,
                                'form': form,
                                'comments': None,  # game_comments
                                'icon_class': 'lg_icon_class_actual_play',
                        }

                return render(request, self.template, context)


class GameResourceView(View):
        def get(self, request, *args, **kwargs):
                if 'mp3' in self.kwargs['filename'] or 'ogg' in self.kwargs['filename']:
                        _type = 'audio/'
                else:
                        _type = 'video/'

                # TODO: Add S3 path
                file_path = settings.MEDIA_ROOT + '/actual_play/' + _type + '/' \
                + self.kwargs['year'] + '/' + self.kwargs['month'] + '/'\
                 + self.kwargs['day'] + \
                '/' + self.kwargs['filename']
                file_wrapper = FileWrapper(open(file_path, 'rb'))
                file_mimetype = mimetypes.guess_type(file_path)
                response = HttpResponse(file_wrapper, content_type=file_mimetype)
                response['X-Sendfile'] = file_path
                response['Content-Length'] = os.stat(file_path).st_size
                response['Content-Diposition'] = 'attachment; filename=%s'\
                 % smart_str(self.kwargs['filename'])
                return response


class GameCommentView(View):
        template = 'actual_play/game.html'

        def post(self, request, *args, **kwargs):
                form = GameCommentForm(request.POST)

                if form.is_valid():
                        comment = form.cleaned_data['comment']
                        user = request.user
                        game = Game.objects.get(pk=request.POST.get('game_id'))
                        group = game.group
                        instance = GameComment(comment=comment, game=game, user=user)
                        instance.save()

                return HttpResponseRedirect(
                        '/actual_play/' + kwargs['group'] + '/' + kwargs['slug'] + '/')


class GameArchiveView(View):
        template = 'actual_play/game_list.html'

        def get(self, request, *args, **kwargs):
            items_recent = Game.objects.filter(active=True,
                                               publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
            items_popular = Game.objects.filter(active=True,
                                                publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
            game_groups = GameGroup.objects.filter(active=True)
            game_types = GameType.objects.filter(active=True)
            game_types_list = []
            game_type = {}

            if self.kwargs:
                if self.kwargs['game_type'] and self.kwargs['game_type'] != None:
                    if GameType.objects.filter(active=True, slug=self.kwargs['game_type']).exists():
                        games = Game.objects.filter(active=True,
                                                    publish_date__lte=datetime.datetime.now(),
                                                    game_type__slug=self.kwargs['game_type']).order_by('-created_date')
                        game_type = GameType.objects.filter(active=True,
                                                            slug=self.kwargs['game_type']).first()
                        game_types_list =  [{'type': game_type, 'games': games}]
                    else:
                        games = Game.objects.filter(active=True,
                                                    publish_date__lte=datetime.datetime.now(),
                                                    group__slug=self.kwargs['game_type']).order_by('-created_date')
                        game_type = GameGroup.objects.filter(active=True,
                                                             slug=self.kwargs['game_type']).first()
                        game_types_list =  [{'type': game_type, 'games': games}]
            else:
                games = Game.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-created_date')
                for group in game_groups:
                    game_type = {
                        'type': group,
                        'games': games.filter(group=group),
                    }
                    game_types_list.append(game_type)

                for game_type in game_types:
                    game_type = {
                        'type': game_type,
                        'games': games.filter(game_type=game_type)
                    }
                    game_types_list.append(game_type)

            links = get_main_links()
            context = {
                'section': { 'name': 'Actual Play' }
            }

            context['game_types'] = game_types_list
            context['og_type'] = 'webpage'
            context['og_url'] = 'http://www.nonhumanuser.com/actual_play/game_archive/'
            context['og_title'] = 'Game Archive'
            context['og_description'] = 'Recorded actual play sessions of Call of Cthulhu and Delta Green.'
            context['og_image'] = 'http://www.nonhumanuser.com//images/Actual_Play.png'
            context['items_recent'] = items_recent
            context['items_popular'] = items_popular
            context['links'] = links
            context['icon_class'] = 'lg_icon_class_actual_play'

            return render(request, self.template, context)
