from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from django.views.generic import View, UpdateView, DetailView
from actual_play.models import GameGroup, Game, Player
from blog.models import Blog, Entry, Category
from library.models import Stack, Item
from itertools import chain
from nonhumanuser.utils import *
from app.utils import get_query
from app.models import Profile
from app.forms import UserForm, ProfileForm
from django.contrib import messages

# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        story = Entry.objects.filter(category__name='Stories', active=True,
                                     publish_date__lte=datetime.datetime.now()).order_by('-created_date').first()
        article = Entry.objects.filter(category__name='Articles', active=True,
                                     publish_date__lte=datetime.datetime.now()).order_by('-created_date').first()
        library_item = Item.objects.filter(active=True,
                                           publish_date__lte=datetime.datetime.now()).order_by('-created_date').first()
        game = Game.objects.filter(active=True,
                                   publish_date__lte=datetime.datetime.now()).order_by('-publish_date').first()
        if game:
            game_group = GameGroup.objects.filter(name=game.group).first()
        else:
            game_group = None
        entry_recent = Entry.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-created_date')
        library_recent = Item.objects.filter(active=True,
                                             publish_date__lte=datetime.datetime.now()).order_by('-created_date')
        games_recent = Game.objects.filter(active=True,
                                           publish_date__lte=datetime.datetime.now()).order_by('-created_date')
        items_recent = list(chain(entry_recent, library_recent, games_recent))
        entry_popular = Entry.objects.filter(active=True,
                                             publish_date__lte=datetime.datetime.now()).order_by('-number_comments')
        library_popular = Item.objects.filter(active=True,
                                              publish_date__lte=datetime.datetime.now()).order_by('-number_comments')
        games_popular = Game.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-number_comments')
        items_popular = list(chain(entry_popular, library_popular, games_popular))
        links = get_main_links()

        context = {
            "site": {
                'title': 'NonHumanUser',
                'description': 'Stories, articles resources and supplements for Call of Cthulhu and related genre games.',
            },
            'og_type': 'webpage',
            'og_url': 'http://www.nonhumanuser.com',
            'og_title': 'NonHumanUser',
            'og_description': 'Stories, articles resources and supplements for Call of Cthulhu and related genre games.',
            'og_image': 'http://www.nonhumanuser.com/images/logo.png',
            'story': story,
            'article': article,
            'library_item': library_item,
            'game': game,
            'game_group': game_group,
            'items_recent': items_recent[0:5],
            'items_popular': items_popular[0:5],
            'section': 'main',
            'links': links,
        }
        return render(request, 'app/index.html', context)


class ProfileView(View):
    """
    Display user profile
    """
    user_form = UserForm
    profile_form = ProfileForm
    initial = {'key': 'value'}
    template_name = 'app/profile.html'

    def get(self, request, *args, **kwargs):
        user_form = self.user_form(initial=self.initial, 
            instance=request.user)
        profile_form = self.profile_form(initial=self.initial,
            instance=request.user.profile)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            })


    def post(self, request, *args, **kwargs):
        user_form = self.user_form(request.POST, instance=request.user)
        profile_form = self.profile_form(request.POST, request.FILES,
            instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile update successful.')
        else:
            messages.error(request, 'Please correct the error below.')

        return render(request, 'app/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            })


class SearchView(View):
    template = 'app/search_results.html'

    def get(self, request, *args, **kwargs):
        query_string = ''
        found_entries = None

        # Sidebar
        entry_recent = Entry.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-created_date')
        library_recent = Item.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-created_date')
        games_recent = Game.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-created_date')
        items_recent = list(chain(entry_recent, library_recent, games_recent))
        entry_popular = Entry.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-number_comments')
        library_popular = Item.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-number_comments')
        games_popular = Game.objects.filter(active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-number_comments')
        items_popular = list(chain(entry_popular, library_popular, games_popular))
        links = get_main_links()

        context = {
            'items_recent': items_recent[0:5],
            'items_popular': items_popular[0:5],
            'links': links,
        }

        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']

            entry_query = get_query(query_string, ['title', 'body',])

            # have to figure out the type here

            entries = Entry.objects.filter(entry_query, active=True,
                                            publish_date__lte=datetime.datetime.now())\
            .order_by('-publish_date')
            items = Item.objects.filter(entry_query, active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-publish_date')
            games = Game.objects.filter(entry_query, active=True,
                                            publish_date__lte=datetime.datetime.now()).order_by('-publish_date')

            found_entries = list(chain(entries, items, games))

        context['query_string'] = query_string
        context['found_entries'] = found_entries
        return render(request, self.template, 
            context, context_instance=RequestContext(request))