from django.contrib import admin
from blog.models import Blog, Entry, EntryComment, Category
from django.db.models import TextField

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
	pass

class EntryAdmin(admin.ModelAdmin):
  pass

class EntryCommentAdmin(admin.ModelAdmin):
	pass

class CategoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryComment, EntryCommentAdmin)
admin.site.register(Category, CategoryAdmin)