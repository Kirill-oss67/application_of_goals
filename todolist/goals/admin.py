from django.contrib import admin

from goals.models import GoalCategory, Goal


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "is_deleted")
    list_display_links = ('title',)
    search_fields = ("title",)
    list_filter = ('is_deleted',)
    readonly_fields = ('created', 'updated',)


class GoalAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "category", 'status', 'priority',)
    list_display_links = ('title',)
    search_fields = ("title", 'description',)
    list_filter = ('status', 'priority',)
    readonly_fields = ('created', 'updated',)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
