from django.forms import ModelForm
from .models import Entry, EntryComment
from django_markdown.widgets import MarkdownWidget


class EntryCommentForm(ModelForm):
  class Meta:
    model = EntryComment
    exclude = ('entry', 'created_date', 'approved', 'author')