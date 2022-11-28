from django.contrib import admin
from . import models

@admin.register(models.Schedule)
class AuthorAdmin(admin.ModelAdmin):
    list_display: ("title", "courses", "slug", "pub_date")
    prepopulated_fields: {
        "slug": ("title",),
    }

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display: ("schedule","name", "content", "pub_date")
    list_filter: ("pub_date")
    search_fields: ("name", "content")

# Register your models here.
