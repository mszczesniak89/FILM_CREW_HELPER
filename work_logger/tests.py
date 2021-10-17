import random
from datetime import timedelta

from django.urls import reverse
from django.test import TestCase, Client
import pytest
from work_logger.models import CrewMember, SubProject, Project, Terms, ShootingDay
from accounts.models import CustomUser
from faker import Faker
faker = Faker("pl_PL")



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
def test_delete_project_view_post_logged_in(user, projects):
    client = Client()
    client.force_login(user)
    old_project_count = len(projects)
    response = client.post(reverse("delete_project_view", kwargs={'pk': projects[0].pk}))
    new_project_count = [project for project in Project.objects.all()]
    assert response.status_code == 302
    assert old_project_count == len(new_project_count) + 1


@pytest.mark.django_db
def test_delete_project_view_post_not_logged_in(user, projects):
    client = Client()
    old_project_count = len(projects)
    response = client.post(reverse("delete_project_view", kwargs={'pk': projects[0].pk}))
    new_project_count = [project for project in Project.objects.all()]
    assert response.status_code == 302
    assert old_project_count == len(new_project_count)


@pytest.mark.django_db
def test_update_project_view_post_logged_in(user, projects):
    client = Client()
    client.force_login(user)
    project = projects[0]
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    response = client.post(reverse('update_project_view', kwargs={'pk': project.pk}),
                           {'name': new_name, 'description': new_description})
    assert response.status_code == 302
    project.refresh_from_db()
    assert project.name == new_name
    assert project.description == new_description


@pytest.mark.django_db
def test_update_project_view_post_not_logged_in(user, projects):
    client = Client()
    project = projects[0]
    old_name = project.name
    old_description = project.description
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    response = client.post(reverse('update_project_view', kwargs={'pk': project.pk}),
                           {'name': new_name, 'description': new_description})
    assert response.status_code == 302
    project.refresh_from_db()
    assert project.name == old_name
    assert project.description == old_description


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
def test_create_subproject_view_get_logged_in(user, projects):
    client = Client()
    client.force_login(user)
    project = projects[0]
    response = client.get(reverse("create-subproject-view", kwargs={'pk': project.pk}))
    assert response.status_code == 200
    assert response.context['form']


@pytest.mark.django_db
def test_create_subproject_view_get_not_logged_in(user, projects):
    client = Client()
    project = projects[0]
    response = client.get(reverse("create-subproject-view", kwargs={'pk': project.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_subproject_view_post_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user)
    subproject = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'parent': projects[0].pk,
        'position': faker.text(max_nb_chars=10),
        'terms': terms[0].pk,
        'crew_members': crew_members[0].pk,
    }
    old_subprojects_count = SubProject.objects.all().count()
    response = client.post(reverse("create-subproject-view", kwargs={'pk': projects[0].pk}), data=subproject)
    assert response.status_code == 302
    new_subprojects_count = SubProject.objects.all()
    assert old_subprojects_count + 1 == new_subprojects_count.count()


@pytest.mark.django_db
def test_create_subproject_view_post_not_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    subproject = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'parent': projects[0].pk,
        'position': faker.text(max_nb_chars=10),
        'terms': terms[0].pk,
        'crew_members': crew_members[0].pk,
    }
    old_subprojects_count = SubProject.objects.all().count()
    response = client.post(reverse("create-subproject-view", kwargs={'pk': projects[0].pk}), data=subproject)
    assert response.status_code == 302
    new_subprojects_count = SubProject.objects.all()
    assert old_subprojects_count == new_subprojects_count.count()


@pytest.mark.django_db
def test_delete_subproject_view_post_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user)
    old_subproject_count = len(subprojects)
    response = client.post(reverse("delete_subproject_view", kwargs={'pk': subprojects[0].pk}))
    new_subproject_count = SubProject.objects.all().count()
    assert response.status_code == 302
    assert old_subproject_count == new_subproject_count + 1


@pytest.mark.django_db
def test_delete_subproject_view_post_not_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    old_subproject_count = len(subprojects)
    response = client.post(reverse("delete_subproject_view", kwargs={'pk': subprojects[0].pk}))
    new_subproject_count = SubProject.objects.all().count()
    assert response.status_code == 302
    assert old_subproject_count == new_subproject_count


@pytest.mark.django_db
def test_update_subproject_view_post_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user)
    subproject = subprojects[0]
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    new_subproject_data = {
        'name': new_name,
        'description': new_description,
        'parent': subproject.parent.pk,
        'position': subproject.position,
        'terms': subproject.terms.pk,
        'crew_members': [crew.pk for crew in subproject.crew_members.all()],
    }
    response = client.post(reverse('update_subproject_view', kwargs={'pk': subproject.pk}), data=new_subproject_data)
    assert response.status_code == 302
    subproject.refresh_from_db()
    assert subproject.name == new_name
    assert subproject.description == new_description


@pytest.mark.django_db
def test_update_subproject_view_post_not_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    subproject = subprojects[0]
    old_name = subproject.name
    old_description = subproject.description
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    new_subproject_data = {
        'name': new_name,
        'description': new_description,
        'parent': subproject.parent.pk,
        'position': subproject.position,
        'terms': subproject.terms.pk,
        'crew_members': [crew.pk for crew in subproject.crew_members.all()],
    }
    response = client.post(reverse('update_subproject_view', kwargs={'pk': subproject.pk}), data=new_subproject_data)
    assert response.status_code == 302
    subproject.refresh_from_db()
    assert subproject.name == old_name
    assert subproject.description == old_description


@pytest.mark.django_db
def test_shooting_days_view_get_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    response = client.get(reverse("shooting-days-view", kwargs={'pk': subprojects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_shooting_days_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user)
    response = client.get(reverse("shooting-days-view", kwargs={'pk': subprojects[0].pk}))
    assert response.status_code == 200
    shooting_days_list = response.context['object_list']
    assert shooting_days_list.count() == len(shooting_days) / 2
    target_shooting_days = ShootingDay.objects.filter(subproject=subprojects[0])
    assert shooting_days_list.count() == target_shooting_days.count()


@pytest.mark.django_db
def test_create_shooting_day_view_post_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user)
    random_date = faker.date_time_this_month()
    end_hour_shift = random_date + timedelta(hours=7)
    shooting_day = {
        'name': faker.text(max_nb_chars=20),
        'date': random_date,
        'start_hour': random_date,
        'end_hour': end_hour_shift,
        'description': faker.text(max_nb_chars=20),
        'ot': random.randint(0, 4),
        'camera_ot': random.randint(0, 3),
        'toc': 0,
        'extras': 0,
        'subproject': subprojects[0].pk
    }
    old_shooting_days_count = ShootingDay.objects.all().count()
    response = client.post(reverse("create-shootingday-view", kwargs={'pk': subprojects[0].pk}), data=shooting_day)
    assert response.status_code == 302
    new_shooting_days_count = ShootingDay.objects.all()
    assert old_shooting_days_count + 1 == new_shooting_days_count.count()


@pytest.mark.django_db
def test_create_shooting_day_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    random_date = faker.date_time_this_month()
    end_hour_shift = random_date + timedelta(hours=7)
    shooting_day = {
        'name': faker.text(max_nb_chars=20),
        'date': random_date,
        'start_hour': random_date,
        'end_hour': end_hour_shift,
        'description': faker.text(max_nb_chars=20),
        'ot': random.randint(0, 4),
        'camera_ot': random.randint(0, 3),
        'toc': 0,
        'extras': 0,
        'subproject': subprojects[0].pk
    }
    old_shooting_days_count = ShootingDay.objects.all().count()
    response = client.post(reverse("create-shootingday-view", kwargs={'pk': subprojects[0].pk}), data=shooting_day)
    assert response.status_code == 302
    new_shooting_days_count = ShootingDay.objects.all()
    assert old_shooting_days_count == new_shooting_days_count.count()


@pytest.mark.django_db
def test_delete_shooting_day_view_post_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user)
    old_shooting_days_count = len(shooting_days)
    response = client.post(reverse("delete_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    new_shooting_days_count = ShootingDay.objects.all().count()
    assert response.status_code == 302
    assert old_shooting_days_count == new_shooting_days_count + 1


@pytest.mark.django_db
def test_delete_shooting_day_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    old_shooting_days_count = len(shooting_days)
    response = client.post(reverse("delete_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    new_shooting_days_count = ShootingDay.objects.all().count()
    assert response.status_code == 302
    assert old_shooting_days_count == new_shooting_days_count


@pytest.mark.django_db
def test_update_shooting_day_view_post_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user)
    shooting_day = shooting_days[0]
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    new_shooting_day_data = {
        'name': new_name,
        'description': new_description,
        'subproject': shooting_day.subproject.pk,
        'date': shooting_day.date,
        'start_hour': shooting_day.start_hour,
        'end_hour': shooting_day.end_hour,
        'ot': shooting_day.ot,
        'camera_ot': shooting_day.camera_ot,
        'toc': shooting_day.toc,
        'extras': shooting_day.extras,
    }
    response = client.post(reverse('update_shootingday_view', kwargs={'pk': shooting_day.pk}),
                           data=new_shooting_day_data)
    assert response.status_code == 302
    shooting_day.refresh_from_db()
    assert shooting_day.name == new_name
    assert shooting_day.description == new_description


@pytest.mark.django_db
def test_update_shooting_day_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    shooting_day = shooting_days[0]
    old_name = shooting_day.name
    old_description = shooting_day.description
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    new_shooting_day_data = {
        'name': new_name,
        'description': new_description,
        'subproject': shooting_day.subproject.pk,
        'date': shooting_day.date,
        'start_hour': shooting_day.start_hour,
        'end_hour': shooting_day.end_hour,
        'ot': shooting_day.ot,
        'camera_ot': shooting_day.camera_ot,
        'toc': shooting_day.toc,
        'extras': shooting_day.extras,
    }
    response = client.post(reverse('update_shootingday_view', kwargs={'pk': shooting_day.pk}),
                           data=new_shooting_day_data)
    assert response.status_code == 302
    shooting_day.refresh_from_db()
    assert shooting_day.name == old_name
    assert shooting_day.description == old_description


@pytest.mark.django_db
def test_shooting_day_detail_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user)
    shooting_day = shooting_days[0]
    response = client.get(reverse("shootingday_detail_view", kwargs={'pk': shooting_day.pk}))
    assert response.status_code == 200
    assert response.context['object']
    shooting_day_data = response.context['object']
    assert shooting_day_data.name
    assert shooting_day_data.date


@pytest.mark.django_db
def test_shooting_day_detail_view_get_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    shooting_day = shooting_days[0]
    response = client.get(reverse("shootingday_detail_view", kwargs={'pk': shooting_day.pk}))
    assert response.status_code == 302













@pytest.mark.django_db
def test_create_terms_view_post_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user)
    new_terms_data = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'pay_period': 1,
        'base_rate': 1500,
        'ot_rate': 35,
        'camera_ot_rate': 50,
        'extras': 0,
        'user': user,
        'working_hours': 1,
    }
    old_terms_count = Terms.objects.all().count()
    response = client.post(reverse("create_terms", kwargs={'pk': projects[0].pk}), data=new_terms_data)
    assert response.status_code == 302
    new_terms_count = Terms.objects.all()
    assert old_terms_count + 1 == new_terms_count.count()




@pytest.mark.django_db
def test_delete_crew_member_view(user, projects, terms, crew_members):
    client = Client()
    client.force_login(user)
    old_crew_members_count = len(crew_members)
    response = client.post(reverse("delete_crew_member", kwargs={'pk': crew_members[0].pk}))
    new_crew_members = [crew_member for crew_member in CrewMember.objects.all()]
    assert response.status_code == 302
    assert old_crew_members_count == len(new_crew_members) + 1

























