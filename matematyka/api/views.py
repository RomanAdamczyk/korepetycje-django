from rest_framework import viewsets
from django.db.models import Count, Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Category, Task, Variable, AdditionalVariable, Issue, UsedVariable, AnswerOption
from .serializers import CategorySerializer, IssueSerializer

import math
import random

# Dozwolone funkcje matematyczne do użycia w eval
allowed_functions = {
    "sqrt": math.sqrt,
    "log": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "abs": abs
}


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
        solutions_map = {}

        for variable in variables:
            try:
                value = float(variable.original_value)
            except ValueError:
                value = variable.original_value

            value_map[variable.name] = value
            
        
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
                result = eval(add_var.formula, allowed_functions, value_map)
            except Exception as e:
                print(f"Błąd w obliczaniu {add_var.name}: {e}")
                continue

            value_map[add_var.name] = result

            if add_var.save_result:
                UsedVariable.objects.create(
                    task=task,
                    issue=issue,
                    variable=None,
                    variable_name=add_var.name,
                    variable_value=str(result)
                )
            
            else:
                solutions_map[add_var.name] = round(result,4)

        print("Rozwiązania:", solutions_map)        
        answer_options_db = AnswerOption.objects.filter(task=task)

        answer_options = []
        for opt in answer_options_db:
            value = solutions_map.get(opt.content)
            if value is not None:
                answer_options.append({
                    'content': str(value),
                    'is_correct': opt.is_correct
                })
        
        serializer = IssueSerializer(issue)
        data = serializer.data
        random.shuffle(answer_options)
        data['answer_options'] = answer_options
        return Response(data, status=status.HTTP_201_CREATED)