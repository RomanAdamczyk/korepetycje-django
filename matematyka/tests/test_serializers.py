import pytest
from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.auth.models import User
from ..models import Category, TaskGroup, TaskLevel, Task, Issue, UserProfile, AssignedTask, Variable, UsedVariable, AnswerOption, UserAnswer, TaskType
from ..api.serializers import CategorySerializer, TaskGroupSerializer, TaskLevelSerializer, TaskSerializer, IssueSerializer, UserProfileSerializer, AssignedTaskSerializer, VariableSerializer, UsedVariableSerializer, AnswerOptionSerializer, UserAnswerSerializer, TaskTypeSerializer

@pytest.mark.django_db
def test_category_serialization():
    category = Category.objects.create(name="Algebra")
    serializer = CategorySerializer(category)
    assert serializer.data['name'] == "Algebra"

@pytest.mark.django_db
def test_category_deserialization():
    data = {'name': "Geometria"}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid()
    category = serializer.save()
    assert category.name == "Geometria"

@pytest.mark.django_db
def test_task_group_serialization():
    task_group = TaskGroup.objects.create(shared_content="Dany jest prostokąt ABCD")
    serializer = TaskGroupSerializer(task_group)
    assert serializer.data['shared_content'] == "Dany jest prostokąt ABCD"

@pytest.mark.django_db
def test_task_group_deserialization():
    data = {'shared_content': "Dany jest trójkąt ABC"}
    serializer = TaskGroupSerializer(data=data)
    assert serializer.is_valid()
    task_group = serializer.save()
    assert task_group.shared_content == "Dany jest trójkąt ABC"

@pytest.mark.django_db
def test_task_level_serialization():
    task_level = TaskLevel.objects.create(exam_level="Matura podstawowa", school_level="Szkoła średnia", class_number=2)
    serializer = TaskLevelSerializer(task_level)
    assert serializer.data['exam_level'] == "Matura podstawowa"
    assert serializer.data['school_level'] == "Szkoła średnia"
    assert serializer.data['class_number'] == 2

@pytest.mark.django_db
def test_task_level_deserialization():
    data = {'exam_level': "Matura rozszerzona", 'school_level': "Szkoła średnia", 'class_number': 3}
    serializer = TaskLevelSerializer(data=data)
    assert serializer.is_valid()
    task_level = serializer.save()
    assert task_level.exam_level == "Matura rozszerzona"
    assert task_level.school_level == "Szkoła średnia"
    assert task_level.class_number == 3

@pytest.mark.django_db
def test_task_serialization():
    category = Category.objects.create(name="Geometria")
    task_group = TaskGroup.objects.create(shared_content="Dany jest prostokąt ABCD")
    task_level = TaskLevel.objects.create(exam_level="Matura podstawowa", school_level="Szkoła średnia", class_number=2)
    task_type = TaskType.objects.create(name="Zadanie otwarte")
    
    task = Task.objects.create(
        content="Oblicz pole prostokąta",
        points=1,
        task_group=task_group,
        task_level=task_level,
        task_type=task_type,
        exam_date=make_aware(datetime(2023, 6, 1)),
        source="CKE"
    )
    task.category.set([category])
    
    serializer = TaskSerializer(task)
    
    assert serializer.data['content'] == "Oblicz pole prostokąta"
    assert serializer.data['points'] == 1
    assert any(cat['name'] == "Geometria" for cat in serializer.data['category']) 
    assert serializer.data['task_group']['shared_content'] == "Dany jest prostokąt ABCD"
    assert serializer.data['task_level']['exam_level'] == "Matura podstawowa"

@pytest.mark.django_db
def test_task_deserialization():
    category = Category.objects.create(name="Geometria")
    task_group = TaskGroup.objects.create(shared_content="Dany jest prostokąt ABCD")
    task_level = TaskLevel.objects.create(exam_level="Matura podstawowa", school_level="Szkoła średnia", class_number=2)
    task_type = TaskType.objects.create(name="Zadanie otwarte")
    
    data = {
        'content': "Oblicz pole kwadratu",
        'points': 2,
        'category_ids': [category.id],
        'task_group_id': task_group.id,
        'task_level_id': task_level.id,
        'task_type_id': task_type.id,
        'exam_date': make_aware(datetime(2023, 6, 1)),
        'source': "CKE"
    }
    
    serializer = TaskSerializer(data=data)
    assert serializer.is_valid()
    task = serializer.save()
    task.category.set(data["category_ids"])

    assert task.content == "Oblicz pole kwadratu"
    assert task.points == 2
    assert task.category.first().name == "Geometria"  
    assert task.task_group.shared_content == "Dany jest prostokąt ABCD"
    assert task.task_level.exam_level == "Matura podstawowa"

@pytest.mark.django_db
def test_issue_serialization():
    category = Category.objects.create(name="Algebra")
    task_group = TaskGroup.objects.create(shared_content="Dany jest prostokąt ABCD")
    task_level = TaskLevel.objects.create(exam_level="Matura podstawowa", school_level="Szkoła średnia", class_number=2)
    
    task = Task.objects.create(
        content="Oblicz pole prostokąta",
        points=1,
        task_group=task_group,
        task_level=task_level,
        exam_date=make_aware(datetime(2023, 6, 1)),
        source="CKE"
    )
    task.category.set([category])
    
    issue = Issue.objects.create(task=task)
    
    serializer = IssueSerializer(issue)
    assert serializer.data['task']['content'] == "Oblicz pole prostokąta"

@pytest.mark.django_db
def test_user_profile_serialization():
    user = User.objects.create_user(username='testuser', password='12345')
    profile = UserProfile.objects.create(user=user, username_for_admin='Test User')
    
    serializer = UserProfileSerializer(profile)
    assert serializer.data['username_for_admin'] == 'Test User'
    assert serializer.data['user'] == user.id

@pytest.mark.django_db
def test_userprofile_deserialization():
    user = User.objects.create_user(username='testuser', password='pass')
    data = {
        'user': user.id,
        'username_for_admin': 'testuser_admin'
    }
    serializer = UserProfileSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    profile = serializer.save()
    assert profile.user == user
    assert profile.username_for_admin == 'testuser_admin'

@pytest.mark.django_db
def test_assigned_task_serialization():
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Algebra")
    task_group = TaskGroup.objects.create(shared_content="Dany jest prostokąt ABCD")
    task_level = TaskLevel.objects.create(exam_level="Matura podstawowa", school_level="Szkoła średnia", class_number=2)
    task_type = TaskType.objects.create(name="Zadanie otwarte")
    
    task = Task.objects.create(
        content="Oblicz pole prostokąta",
        points=1,
        task_group=task_group,
        task_level=task_level,
        task_type=task_type,
        exam_date=make_aware(datetime(2023, 6, 1)),
        source="CKE"
    )
    task.category.set([category])
    
    assigned_task = AssignedTask.objects.create(user=user, task=task, assigned_date=make_aware(datetime(2023, 5, 1)), deadline=make_aware(datetime(2023, 6, 1)))
    
    serializer = AssignedTaskSerializer(assigned_task)
    assert serializer.data['user'] == user.id
    assert serializer.data['task']['content'] == "Oblicz pole prostokąta"

@pytest.mark.django_db
def test_assigned_task_deserialization():
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Algebra")
    task_group = TaskGroup.objects.create(shared_content="Dany jest prostokąt ABCD")
    task_level = TaskLevel.objects.create(exam_level="Matura podstawowa", school_level="Szkoła średnia", class_number=2)
    
    task = Task.objects.create(
        content="Oblicz pole prostokąta",
        points=1,
        task_group=task_group,
        task_level=task_level,
        exam_date=make_aware(datetime(2023, 6, 1)),
        source="CKE"
    )
    task.category.set([category])
    
    data = {
        'user': user.id,
        'task_id': task.id,
        'assigned_date': make_aware(datetime(2023, 5, 1)),
        'deadline': make_aware(datetime(2023, 6, 1))
    }
    
    serializer = AssignedTaskSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assigned_task = serializer.save()

    assigned_task.task = task
    assigned_task.save()

    assert assigned_task.user == user
    assert assigned_task.task.content == "Oblicz pole prostokąta"