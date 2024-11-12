from django.contrib import admin
from .models import Assignment

# admin things go here

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'industry', 'duration', 'rate', 'currency', 'is_active', 'created_by', 'created_at')
    list_filter = ('industry', 'is_active', 'created_at')
    search_fields = ('title', 'description')