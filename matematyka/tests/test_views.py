import pytest
from ..models import Category

@pytest.mark.django_db
class TestCategoryViews:

    def test_category_list_view(self, client):
        response = client.get('/matematyka/categories/')
        assert response.status_code == 200
        assert 'categories' in response.context

    # def test_category_detail_view(self, client):
    #     category = Category.objects.create(name="Test Category")
    #     response = client.get(f'/categories/{category.id}/')
    #     assert response.status_code == 200
    #     assert response.context['category'].name == "Test Category"

    # def test_category_detail_view_not_found(self, client):
    #     response = client.get('/categories/9999/')
    #     assert response.status_code == 404