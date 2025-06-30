import requests
from django.views.generic import TemplateView
from .models import Task

class CategoryListView(TemplateView):
    template_name = 'matematyka/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get('http://localhost:8000/api/categories/', cookies=self.request.COOKIES)
        if response.status_code == 200:
            context['categories'] = response.json()
        else:
            context['categories'] = []
        return context
    
class CategoryTasksView(TemplateView):
    template_name = 'matematyka/category_tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        response = requests.get(f'http://localhost:8000/api/categories/{category_id}/', cookies=self.request.COOKIES)
        if response.status_code == 200:
            context['category'] = response.json()
            context['tasks'] = context['category'].get('tasks', [])
        else:
            context['category'] = None
            context['tasks'] = []
    
        return context
