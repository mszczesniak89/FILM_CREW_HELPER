from django.test import TestCase, Client
import pytest
from work_logger.models import CrewMember, SubProject, Project

# Create your tests here.
from django.urls import reverse


def test_index_view_get():
    client = Client()
    response = client.get(reverse("index-view"))
    assert response.status_code == 200


def test_index_view_post():
    client = Client()
    response = client.post(reverse("index-view"))
    assert response.status_code == 200


def test_about_view_get():
    client = Client()
    response = client.get(reverse("about-page"))
    assert response.status_code == 200


def test_about_view_post():
    client = Client()
    response = client.post(reverse("about-page"))
    assert response.status_code == 200


def test_contact_view_get():
    client = Client()
    response = client.get(reverse("contact-page"))
    assert response.status_code == 200


def test_contact_view_post():
    client = Client()
    response = client.post(reverse("contact-page"))
    assert response.status_code == 200



@pytest.mark.django_db
def test_main_page_view_get_not_logged_in():
    client = Client()
    response = client.get(reverse("main-page"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_main_page_view_get_logged_in(user):
    client = Client()
    client.force_login(user)
    response = client.get(reverse("main-page"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_subprojects_view_get_not_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    response = client.get(reverse("subprojects-view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_subprojects_view_get_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user)
    response = client.get(reverse("subprojects-view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 200
    subprojects_list = response.context['object_list']
    assert subprojects_list.count() == len(subprojects)/2
    target_subprojects = SubProject.objects.filter(parent=projects[0])
    assert subprojects_list.count() == target_subprojects.count()


@pytest.mark.django_db
def test_create_project_view_get_logged_in(user):
    client = Client()
    client.force_login(user)
    response = client.get(reverse("create-project-view"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_project_view_get_not_logged_in(user):
    client = Client()
    response = client.get(reverse("create-project-view"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_project_view_post_logged_in(user, projects):
    client = Client()
    client.force_login(user)
    project = {
        'name': 'Xxxxx',
        'description': 'xxxxx',
        'user': user
    }
    old_projects_count = len(projects)
    response = client.post(reverse("create-project-view"), data=project)
    assert response.status_code == 302
    new_projects_count = Project.objects.filter(user=user)
    assert old_projects_count + 1 == new_projects_count.count()


@pytest.mark.django_db
def test_create_project_view_post_not_logged_in(user, projects):
    client = Client()
    project = {
        'name': 'Xxxxx',
        'description': 'xxxxx',
        'user': user
    }
    old_projects_count = len(projects)
    response = client.post(reverse("create-project-view"), data=project)
    assert response.status_code == 302
    new_projects_count = Project.objects.filter(user=user)
    assert old_projects_count == new_projects_count.count()








@pytest.mark.django_db
def test_delete_crew_member(user, projects, terms, crew_members):
    client = Client()
    client.force_login(user)
    old_crew_members_count = len(crew_members)
    response = client.post(reverse("delete_crew_member", kwargs={'pk': crew_members[0].pk}))
    new_crew_members = [crew_member for crew_member in CrewMember.objects.all()]
    assert response.status_code == 302
    assert old_crew_members_count == len(new_crew_members) + 1






















