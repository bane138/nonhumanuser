from django.contrib import admin
from library.models import Stack, Item, ItemType, ItemComment

# Register your models here.
class StackAdmin(admin.ModelAdmin):
  pass


class ItemAdmin(admin.ModelAdmin):
  pass


class ItemTypeAdmin(admin.ModelAdmin):
  pass


class ItemCommentAdmin(admin.ModelAdmin):
  pass


admin.site.register(Stack, StackAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(ItemComment, ItemCommentAdmin)