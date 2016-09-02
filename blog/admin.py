from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from blog.models import Blog, Entry, EntryComment, Category

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
	pass

class EntryAdmin(MarkdownModelAdmin):
	pass

class EntryCommentAdmin(admin.ModelAdmin):
	pass

class CategoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, MarkdownModelAdmin)
admin.site.register(EntryComment, EntryCommentAdmin)
admin.site.register(Category, CategoryAdmin)