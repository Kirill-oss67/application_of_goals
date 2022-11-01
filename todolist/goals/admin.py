from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


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


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "text",)
    list_display_links = ('text',)
    search_fields = ("text",)
    readonly_fields = ('created', 'updated',)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
