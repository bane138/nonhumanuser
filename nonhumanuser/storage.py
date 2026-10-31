from whitenoise.storage import CompressedManifestStaticFilesStorage


class LenientManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Hashed static files, but a missing file renders as its plain URL instead of a server error.

    Some templates build image names from data (images/<section name>.png), so a section
    without a matching image should show a broken image, as it did before, not a 500.
    """

    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            return name
