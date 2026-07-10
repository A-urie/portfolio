from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'order', 'project_date')
    list_filter = ('category', 'featured')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)