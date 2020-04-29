from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):

    def created_date(self, obj):
        return obj.created.strftime("%Y %b %d, %p %I:%M")

    def schedule_date(self, obj):
        return obj.created.strftime("%Y %b %d, %p %I:%M")

    readonly_fields = ['created_date']
    list_display = ['user', 'title', 'important', 'schedule_date', 'created_date', 'date_completed']
    list_display_links = ['title']