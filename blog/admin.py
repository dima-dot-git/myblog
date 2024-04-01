from django.contrib import admin
from .models import Post, Category, Tag, Subscribe, Comment,PostsPhoto, Profile_WER

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Subscribe)
admin.site.register(Comment)
admin.site.register(PostsPhoto)
admin.site.register(Profile_WER)
