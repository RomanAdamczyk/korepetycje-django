from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:category_id>/', views.CategoryTasksView.as_view(), name='category_tasks'),
    # path('task/<int:pk>/', views.IssueDetailView.as_view(),name='issue_detail')
    path('task/<int:issue_id>/', views.start_task_view, name='start-task'),
]
