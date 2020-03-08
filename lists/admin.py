from django.contrib import admin

from lists.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
