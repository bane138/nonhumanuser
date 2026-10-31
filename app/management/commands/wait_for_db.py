import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Block until the database accepts connections."

    def add_arguments(self, parser):
        parser.add_argument("--timeout", type=int, default=60)

    def handle(self, *args, timeout, **options):
        deadline = time.monotonic() + timeout
        while True:
            try:
                connection.ensure_connection()
                break
            except OperationalError:
                if time.monotonic() > deadline:
                    raise
                self.stdout.write("Waiting for database...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available."))
