from django.db import migrations

BASE = "https://s3-us-west-2.amazonaws.com/nonhumanuser/actual_plays/"
BROKEN = BASE + "BrockfordHouse.mp3" + BASE + "BeneathYou-part3.mp3"


def fix_audio_url(apps, schema_editor):
    """'Beneath You Part 3' had the Brockford House URL pasted in front of its own mp3 URL."""
    Game = apps.get_model("actual_play", "Game")
    Game.objects.filter(audio_url_mp3=BROKEN).update(audio_url_mp3=BASE + "BeneathYou-part3.mp3")


class Migration(migrations.Migration):

    dependencies = [
        ("actual_play", "0002_reconcile_gamegroup"),
    ]

    operations = [
        migrations.RunPython(fix_audio_url, migrations.RunPython.noop),
    ]
