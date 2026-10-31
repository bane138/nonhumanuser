from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Write, publicly fetch, and delete a test file using the configured media storage (e.g. S3)."

    def handle(self, *args, **options):
        self.stdout.write(f"Storage backend: {settings.STORAGES['default']['BACKEND']}")
        if not settings.AWS_STORAGE_BUCKET_NAME:
            self.stdout.write(self.style.WARNING("AWS_STORAGE_BUCKET_NAME is not set; using local disk."))
        else:
            self.stdout.write(f"Bucket: {settings.AWS_STORAGE_BUCKET_NAME} ({settings.AWS_S3_REGION_NAME})")

        try:
            name = default_storage.save("storage-check/test.txt", ContentFile(b"storage check"))
        except Exception as exc:
            raise CommandError(f"Upload failed (check keys, bucket name, region, IAM policy): {exc}") from exc
        self.stdout.write(self.style.SUCCESS(f"Uploaded {name}"))

        try:
            url = default_storage.url(name)
            if url.startswith("http"):
                try:
                    with urlopen(url, timeout=10) as resp:
                        public_ok = resp.read() == b"storage check"
                except (HTTPError, URLError) as exc:
                    raise CommandError(
                        f"Uploaded, but {url} is not publicly readable ({exc}). "
                        "Check the bucket policy and the Block Public Access settings."
                    ) from exc
                if not public_ok:
                    raise CommandError(f"{url} returned unexpected content.")
                self.stdout.write(self.style.SUCCESS(f"Publicly readable at {url}"))
        finally:
            default_storage.delete(name)
        self.stdout.write(self.style.SUCCESS("Deleted test file. Storage is working."))
