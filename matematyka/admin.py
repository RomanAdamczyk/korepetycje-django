from django.contrib import admin
from matematyka.models import Category, TaskGroup, TaskLevel, Task, Issue, UserProfile, AssignedTask, Variable, UsedVariable, AnswerOption, UserAnswer, TaskType, AdditionalVariable, Source

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'shared_content']
    search_fields = ['shared_content']

class TaskLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'exam_level', 'school_level', 'class_number']
    search_fields = ['exam_level', 'school_level']

class SourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'points', 'exam_date', 'source', 'hint', 'sub_number']
    search_fields = ['content', 'source']
    list_filter = ['exam_date', 'category', 'task_group', 'task_level']
    filter_horizontal = ['category']

class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'task']
    search_fields = ['task__content']
    list_filter = ['task']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'username_for_admin']
    search_fields = ['user__username', 'username_for_admin']

class AssignedTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'task', 'assigned_date', 'deadline']
    search_fields = ['user__username', 'task__content']
    list_filter = ['assigned_date', 'deadline']

class VariableAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'min_value', 'max_value','step','choices', 'original_value']
    search_fields = ['name']
    list_filter = ['min_value', 'max_value']

class AdditionalVariableAdmin(admin.ModelAdmin):
    list_display = ['id', 'task__id', 'name', 'formula', 'save_result']

class UsedVariableAdmin(admin.ModelAdmin):
    list_display = ['id', 'variable', 'issue', 'variable_name', 'variable_value']
    search_fields = ['variable__variable_name', 'issue__task__content']
    list_filter = ['issue']

class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'task__id','content', 'is_correct']
    search_fields = ['task__content', 'content']
    list_filter = ['is_correct']

class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# class UserAnswerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'get_task', 'get_answer_option', 'is_correct']
    
#     def get_task(self, obj):
#         return obj.answer_option.task if obj.answer_option else None
#     get_task.short_description = 'Task'
    
#     def get_answer_option(self, obj):
#         return obj.answer_option.content if obj.answer_option else None
#     get_answer_option.short_description = 'Answer Option'

#     search_fields = ['user__username', 'answer_option__task__content', 'answer_option__content']
#     list_filter = ['is_correct']

admin.site.register(Category, CategoryAdmin)
admin.site.register(TaskGroup, TaskGroupAdmin) 
admin.site.register(TaskLevel, TaskLevelAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AssignedTask, AssignedTaskAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(AdditionalVariable, AdditionalVariableAdmin)
admin.site.register(UsedVariable, UsedVariableAdmin)
admin.site.register(AnswerOption, AnswerOptionAdmin)
admin.site.register(UserAnswer)
admin.site.register(TaskType, TaskTypeAdmin)