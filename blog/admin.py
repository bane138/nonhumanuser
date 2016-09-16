from django.contrib import admin
from blog.models import Blog, Entry, EntryComment, Category
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
	pass

class EntryAdmin(MarkdownModelAdmin):
  formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}
  pass

class EntryCommentAdmin(admin.ModelAdmin):
	pass

class CategoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryComment, EntryCommentAdmin)
admin.site.register(Category, CategoryAdmin)