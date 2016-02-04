from django.contrib import admin
from blog.models import Blog, Entry, Category

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
	pass

class EntryAdmin(admin.ModelAdmin):
	pass

class CategoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)