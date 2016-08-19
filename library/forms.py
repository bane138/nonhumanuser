from django.forms import ModelForm
from .models import Item, ItemComment

class ItemCreateForm(ModelForm):
	class Meta:
		model = Item
		exclude = ('slug',)


class ItemCommentForm(forms.ModelForm):
	class Meta:
		model = ItemComment
		fields = ('author', 'body'	)