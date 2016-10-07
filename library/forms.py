from django.forms import ModelForm
from .models import Item, ItemComment

class ItemCreateForm(ModelForm):
  class Meta:
    model = Item
    exclude = ('slug',)


class ItemCommentForm(ModelForm):
  class Meta:
    model = ItemComment
    exclude = ('item', 'created_date', 'approved', 'user')