"""Copy a local media folder into the S3 media bucket, keeping each file's name.

FileField values are paths relative to the media root (e.g. "entry/2016/12/08/foo.png"),
so files uploaded under the same names need no database changes. Safe to re-run: files
already in the bucket with the same size are skipped.
"""

import mimetypes
from pathlib import Path

import boto3
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import models


class Command(BaseCommand):
    help = "Upload a local media folder to the S3 media bucket, then check every database file reference."

    def add_arguments(self, parser):
        parser.add_argument("source", help="Local folder laid out like MEDIA_ROOT")
        parser.add_argument("--only-referenced", action="store_true",
                            help="Upload only files the database refers to")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, source, only_referenced, dry_run, **options):
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")
        if not bucket:
            raise CommandError("AWS_STORAGE_BUCKET_NAME is not set.")
        root = Path(source)
        if not root.is_dir():
            raise CommandError(f"{root} is not a folder.")
        prefix = settings.AWS_LOCATION.strip("/") + "/"
        s3 = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        existing = {}
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                existing[obj["Key"]] = obj["Size"]

        referenced = self.referenced_names()
        files = sorted(p for p in root.rglob("*") if p.is_file())
        if only_referenced:
            files = [p for p in files if p.relative_to(root).as_posix() in referenced]

        uploaded = skipped = 0
        for path in files:
            name = path.relative_to(root).as_posix()
            key = prefix + name
            size = path.stat().st_size
            if existing.get(key) == size:
                skipped += 1
                continue
            content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
            self.stdout.write(f"{'Would upload' if dry_run else 'Uploading'} {name} ({size / 1e6:.1f} MB)")
            if not dry_run:
                s3.upload_file(str(path), bucket, key, ExtraArgs={
                    "ContentType": content_type, **settings.AWS_S3_OBJECT_PARAMETERS,
                })
                existing[key] = size
            uploaded += 1

        missing = sorted(n for n in referenced if prefix + n not in existing)
        self.stdout.write(f"Uploaded {uploaded}, already there {skipped}.")
        if missing:
            self.stdout.write(self.style.WARNING(f"{len(missing)} database file references are not in the bucket:"))
            for name in missing:
                self.stdout.write(f"  {name}")
        else:
            self.stdout.write(self.style.SUCCESS(f"All {len(referenced)} database file references are in the bucket."))

    @staticmethod
    def referenced_names():
        names = set()
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if isinstance(field, models.FileField):
                    names.update(model.objects.exclude(**{field.name: ""}).exclude(**{f"{field.name}__isnull": True})
                                 .values_list(field.name, flat=True))
        return names
