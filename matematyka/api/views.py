from rest_framework import viewsets
from django.db.models import Count, Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import redirect

from ..models import Category, Task, Variable, AdditionalVariable, Issue, UsedVariable, AnswerOption
from .serializers import CategorySerializer, IssueSerializer

import random

from sympy import sympify, N

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
            expr = sympify(add_var.formula)
            evaluated = expr.subs(value_map)
            numeric_result = round(float(N(evaluated)),4)  
            
            value_map[add_var.name] = numeric_result
            
            if add_var.save_result:
                UsedVariable.objects.create(
                    task=task,
                    issue=issue,
                    variable=None,
                    variable_name=add_var.name,
                    variable_value=str(numeric_result)
                )
            else:           
                solutions_map[add_var.name] = {
                    "symbolic": str(expr),
                    "numeric": numeric_result
                }

        answer_options_db = AnswerOption.objects.filter(task=task)

        answer_options = []

        for opt in answer_options_db:
            solution = solutions_map.get(opt.content)
            if solution:
                if opt.display_format == 'symbolic':
                    content = solution['symbolic']
                elif opt.display_format == 'numeric':
                    content = str(solution['numeric'])
                else:
                    print("Nieznany format odpowiedzi:", opt.display_format)

                answer_options.append({
                    'content': content,
                    'is_correct': opt.is_correct,
                    'format': opt.display_format
                })        
        serializer = IssueSerializer(issue)
        data = serializer.data
        random.shuffle(answer_options)
        data['answer_options'] = answer_options
        # return Response(data, status=status.HTTP_201_CREATED)
        return redirect('start-task', issue_id=issue.id)

    
class IssueDetailAPI(generics.RetrieveAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer