from django.contrib import admin

from base.admin import BaseModelAdmin

from .models import List


@admin.register(List)
class ListAdmin(BaseModelAdmin):
    list_display = ['_is_active', 'created_at', 'name', 'owner']
    list_filter = ['owner', ]



