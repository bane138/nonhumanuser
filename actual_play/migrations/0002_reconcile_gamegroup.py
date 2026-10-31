from django.db import migrations


class Migration(migrations.Migration):
    """Bring the production gamegroup table in line with the model.

    Production carried an unused, empty "group" column and a NOT NULL game_type from
    migrations that were never committed. Both statements are no-ops on a fresh database.
    """

    dependencies = [
        ("actual_play", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                'ALTER TABLE actual_play_gamegroup DROP COLUMN IF EXISTS "group"',
                "ALTER TABLE actual_play_gamegroup ALTER COLUMN game_type DROP NOT NULL",
            ],
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
