from django.forms import ModelForm
from .models import Entry
from django_markdown.widgets import MarkdownWidget

class EntryCreateForm(ModelForm):
  body = forms.CharField(widget=MarkdownWidget())
	class Meta:
		model = Entry
		exclude = ('slug',)