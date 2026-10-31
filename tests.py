"""Smoke tests: every public page renders, and old /media/ links redirect to storage."""

from datetime import datetime, timedelta

import pytest
from django.core.management import call_command

from actual_play.models import Game, GameGroup, GameType
from blog.models import Blog, Category, Entry
from library.models import Item, ItemType, Stack

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _local_storage(settings, tmp_path):
    settings.STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    settings.MEDIA_ROOT = tmp_path / "media"
    settings.SECURE_SSL_REDIRECT = False


@pytest.fixture
def content():
    now = datetime.now()
    past = now - timedelta(days=1)
    blog = Blog.objects.create(name="NHU", tagline="", created_date=now)
    stories = Category.objects.create(name="Stories", created_date=now, active=True)
    articles = Category.objects.create(name="Articles", created_date=now, active=True)
    story = Entry.objects.create(blog=blog, category=stories, title="The Seed Man", body="Cthulhu stirs",
                                 active=True, created_date=now, modified_date=now, publish_date=past)
    article = Entry.objects.create(blog=blog, category=articles, title="Friend or Foe", body="An article",
                                   active=True, created_date=now, modified_date=now, publish_date=past)
    stack = Stack.objects.create(name="Locations", tagline="Places", created_date=now, modified_date=now)
    item_type = ItemType.objects.create(name="Locations", created_date=now, modified_date=now)
    item = Item.objects.create(stack=stack, item_type=item_type, title="Lighthouse", body="A map", active=True,
                               created_date=now, modified_date=now, publish_date=past)
    group = GameGroup.objects.create(name="Cult of Chaos", created_date=now, last_played=now, status="active")
    game_type = GameType.objects.create(name="Call of Cthulhu Classic", created_date=now, modified_date=now,
                                        active=True)
    game = Game.objects.create(title="Masks Part 1", group=group, game_type=game_type, active=True,
                               created_date=now, modified_date=now, publish_date=past)
    return {"story": story, "article": article, "stack": stack, "item": item, "game": game,
            "game_type": game_type}


def test_public_pages_render(client, content):
    urls = [
        "/", "/stories/", "/articles/", "/library/", "/actual_play/",
        "/stories/story_archive/", "/articles/article_archive/", "/library/library_archive/",
        "/actual_play/game_archive/", "/blog/", "/search/?q=cthulhu",
        "/members/login/", "/accounts/register/", "/admin/login/",
        content["story"].get_absolute_url(), content["article"].get_absolute_url(),
        f"/library/{content['stack'].slug}/", content["item"].get_absolute_url(),
        f"/actual_play/{content['game_type'].slug}/", content["game"].get_absolute_url(),
    ]
    for url in urls:
        assert client.get(url).status_code == 200, url


def test_search_finds_entries(client, content):
    resp = client.get("/search/?q=Cthulhu")
    assert "The Seed Man" in resp.content.decode()


@pytest.mark.parametrize("old_url, name", [
    ("/media/library/item/2016/10/18/Nitty_Bau.pdf", "library/item/2016/10/18/Nitty_Bau.pdf"),
    ("/media/actual_play/audio/2016/10/25/TheMadman.mp3", "actual_play/audio/2016/10/25/TheMadman.mp3"),
])
def test_old_media_links_redirect_to_storage(client, settings, old_url, name):
    settings.MEDIA_URL = "https://bucket.example.com/media/"
    resp = client.get(old_url)
    assert resp.status_code == 302
    assert resp["Location"] == f"https://bucket.example.com/media/{name}"


def test_models_match_migrations():
    call_command("makemigrations", "--check", "--dry-run", verbosity=0)
