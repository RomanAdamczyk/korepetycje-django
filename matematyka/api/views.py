from rest_framework import viewsets
from django.db.models import Count, Prefetch
from ..models import Category, Task
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(tasks_count=Count('tasks')).prefetch_related(
        Prefetch('tasks', queryset=Task.objects.all())
    )
    serializer_class = CategorySerializer
