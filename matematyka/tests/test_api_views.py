import pytest
from django.contrib.auth.models import User

from ..models import Category, Task
from ..api.serializers import CategorySerializer
from ..api.views import CategoryViewSet

@pytest.mark.django_db
class TestCategoryAPI:

    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_category_viewset_list(self, client):
        client.login(username='testuser', password='testpass')
        category = Category.objects.create(name="Test Category")
        task1 = Task.objects.create(content="Zadanie 1")
        task1.category.add(category)
        task2 = Task.objects.create(content="Zadanie 2")
        task2.category.add(category)

        response = client.get('/api/categories/')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == "Test Category"
        assert data[0]['tasks_count'] == 2
        assert data[0]['tasks'][0]['content'] == "Zadanie 1"
        assert data[0]['tasks'][1]['content'] == "Zadanie 2"

    def test_retrieve_category(self, client):
        client.login(username='testuser', password='testpass')

        category = Category.objects.create(name="Test Category")
        task1 = Task.objects.create(content="Zadanie 1")
        task1.category.add(category)
        task2 = Task.objects.create(content="Zadanie 2")
        task2.category.add(category)

        response = client.get(f'/api/categories/{category.id}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == "Test Category"
        assert data['tasks_count'] == 2
        assert len(data['tasks']) == 2
        assert data['tasks'][0]['content'] == "Zadanie 1"
        assert data['tasks'][1]['content'] == "Zadanie 2"

    def test_retrieve_category_not_found(self, client):
        client.login(username='testuser', password='testpass')
        response = client.get('/api/categories/9999/') 
        assert response.status_code == 404  

    def test_list_categories_empty(self, client):
        client.login(username='testuser', password='testpass')
        response = client.get('/api/categories/')
        data = response.json()
        assert response.status_code == 200
        assert data == [] 

    def test_retrieve_category_with_no_tasks(self, client):
        client.login(username='testuser', password='testpass')
        category = Category.objects.create(name="Empty Category")
        
        response = client.get(f'/api/categories/{category.id}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == "Empty Category"
        assert data['tasks_count'] == 0
        assert data['tasks'] == []