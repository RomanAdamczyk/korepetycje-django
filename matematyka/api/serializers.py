from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Category, TaskGroup, TaskLevel, Task, Issue, UserProfile, AssignedTask, Variable, UsedVariable, AnswerOption, UserAnswer, TaskType

class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ['id', 'shared_content']

class TaskLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLevel
        fields = ['id', 'exam_level', 'school_level', 'class_number']

class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, write_only=True, source='category')
    task_group = TaskGroupSerializer(read_only=True, required=False)
    task_group_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskGroup.objects.all(), write_only=True, source='task_group', required=False)
    task_level = TaskLevelSerializer(read_only=True)
    task_level_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskLevel.objects.all(), write_only=True, source='task_level', required=False)
    task_type = TaskTypeSerializer(read_only=True, required=False)
    task_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskType.objects.all(), write_only=True, source='task_type', required=False)
    source = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ['id', 'content', 'points', 'category','category_ids', 'task_group','task_group_id', 'task_level','task_level_id', 'exam_date', 'source', 'hint', 'sub_number','task_type','task_type_id']

class CategorySerializer(serializers.ModelSerializer):
    tasks_count = serializers.IntegerField(read_only=True)
    tasks = serializers.SerializerMethodField()
    class Meta: 
        model = Category
        fields = ['id', 'name', 'tasks_count','tasks']

    def get_tasks(self, obj):
        return TaskSerializer(obj.tasks.all(), many=True).data

class IssueSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'task']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username_for_admin']

class AssignedTaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    task = TaskSerializer(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), write_only=True, source='task'
    )    

    class Meta:
        model = AssignedTask
        fields = ['id', 'user', 'task','task_id', 'assigned_date', 'deadline']

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ['id', 'name', 'value', 'description', 'min_value', 'max_value', 'step', 'choices', 'original_value']

class UsedVariableSerializer(serializers.ModelSerializer):
    variable = VariableSerializer(read_only=True)
    issue = IssueSerializer(read_only=True)

    class Meta:
        model = UsedVariable
        fields = ['id', 'issue', 'variable', 'task'] 

class AnswerOptionSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    issue = IssueSerializer(read_only=True)
    
    class Meta:
        model = AnswerOption
        fields = ['id', 'task', 'content', 'is_correct']

class UserAnswerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    task = TaskSerializer(read_only=True)
    answer_option = AnswerOptionSerializer(read_only=True)
    issue = IssueSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['id', 'user', 'task', 'issue', 'answer_option', 'is_correct', 'answer_date', 'used_hint']
