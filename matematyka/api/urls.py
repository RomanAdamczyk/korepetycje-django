from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/<int:pk>/', views.IssueDetailAPIView.as_view(), name='issue-detail'),
    path('tasks/<int:task_id>/start_original_variables/', views.StartIssueOriginalVarables.as_view(), name='start_issue_original_varables'),
    path('api-auth/', include('rest_framework.urls')),
]