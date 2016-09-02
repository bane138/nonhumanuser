from django.contrib import admin
from django_markdown.models import MarkdownField
from django_markdown.admin import MarkdownModelAdmin, AdminMarkdownWidget
from blog.models import Blog, Entry, EntryComment, Category

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
	pass

class EntryAdmin(admin.ModelAdmin):
	formfield_overrides = {MarkdownField: {'widget': AdminMarkdownWidget}}

class EntryCommentAdmin(admin.ModelAdmin):
	pass

class CategoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryComment, EntryCommentAdmin)
admin.site.register(Category, CategoryAdmin)