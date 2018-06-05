from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('created_at', 'updated_at')
