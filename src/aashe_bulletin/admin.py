from django.contrib import admin

from bulletin.models import Category


class CategoryAdmin(admin.ModelAdmin):
    actions = None  # No delete for you!

    list_display = ["fully_qualified_name"]

    fields = ["fully_qualified_name",
              "private",
              "url",
              "image"]

    readonly_fields = ["fully_qualified_name"]

admin.site.register(Category, CategoryAdmin)
