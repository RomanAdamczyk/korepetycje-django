from rest_framework import viewsets
from django.db.models import Count, Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Category, Task, Variable, AdditionalVariable, Issue, UsedVariable
from .serializers import CategorySerializer, IssueSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(tasks_count=Count('tasks')).prefetch_related(
        Prefetch('tasks', queryset=Task.objects.all())
    )
    serializer_class = CategorySerializer

class StartIssueOriginalVarables(APIView):

    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        issue = Issue.objects.create(task=task, variable_is_random=False)

        variables = Variable.objects.filter(task=task)

        value_map = {}

        for variable in variables:
            try:
                value = float(variable.original_value)
            except ValueError:
                value = variable.original_value

            value_map[variable.name] = value
            
            if add_var.save_result:
                UsedVariable.objects.create(
                    task=task,
                    issue=issue,
                    variable=variable,
                    variable_name=variable.name,
                    variable_value=str(value)
                )

        additional_variables = AdditionalVariable.objects.filter(task=task)

        for add_var in additional_variables:
            try:
                result = eval(add_var.formula, {}, value_map)
            except Exception as e:
                print(f"Błąd w obliczaniu {add_var.name}: {e}")
                continue

            value_map[add_var.name] = result

            UsedVariable.objects.create(
                task=task,
                issue=issue,
                variable=None,
                variable_name=add_var.name,
                variable_value=str(result)
             )
        
        serializer = IssueSerializer(issue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)