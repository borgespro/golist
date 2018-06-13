from django.contrib import admin

from base.admin import BaseModelAdmin

from .models import List, Item


class ItemInLine(admin.TabularInline):
    model = Item
    extra = 0


@admin.register(List)
class ListAdmin(BaseModelAdmin):
    list_display = ['_is_active', 'name', 'created_at', 'owner']
    list_display_links = ('name', 'created_at', )
    list_filter = ['owner', ]

    fieldsets = (
        (
            None, {
                'fields': ('owner', 'name', 'valid_at'),
            }
        ),
        (
            'Info', {
                'fields': ('created_at', 'updated_at'),
            }
        ),
    )

    inlines = [
        ItemInLine,
    ]



