from django.forms import ModelForm
from .models import Entry, EntryComment


class EntryCommentForm(ModelForm):
  class Meta:
    model = EntryComment
    exclude = ('entry', 'created_date', 'approved', 'user')