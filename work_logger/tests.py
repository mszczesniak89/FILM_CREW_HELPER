import os

from django.core import mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'FILM_CREW_HELPER.settings'
from datetime import timedelta
from django.urls import reverse
from django.test import TestCase, Client
import pytest
from work_logger.models import CrewMember, SubProject, Project, Terms, ShootingDay
from accounts.models import CustomUser
from faker import Faker
import random
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


def test_login_view_get():
    client = Client()
    response = client.get(reverse("login"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post(user):
    client = Client()
    password = faker.password(length=12)
    user[0].set_password(password)
    user[0].save()
    response = client.post(reverse("login"), {
        'username': user[0].username,
        'password': password
    })
    assert response.status_code == 302


def test_register_view_get():
    client = Client()
    response = client.get(reverse("signup"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_view_post(user):
    client = Client()
    username = faker.word()
    password = faker.password(length=12)
    email = faker.email()
    new_user_data = {
        'username': username,
        'password1': password,
        'password2': password,
        'email': email,
    }
    old_user_count = CustomUser.objects.all().count()
    response = client.post(reverse("signup"), data=new_user_data)
    new_user_count = CustomUser.objects.all().count()
    assert response.status_code == 302
    assert old_user_count + 1 == new_user_count


def test_reset_password_view_get():
    client = Client()
    response = client.get(reverse("password_reset"))
    assert response.status_code == 200


def test_reset_password_view_post():
    client = Client()
    response = client.get(reverse("password_reset"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_reset_password_view_post_correct_email_address(user, projects):
    client = Client()
    user_email = user[0].email
    response = client.post(reverse("password_reset"), {'email': user_email})
    assert response.status_code == 302
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_reset_password_view_post_wrong_email_address(user, projects):
    client = Client()
    user_email = faker.email()
    response = client.post(reverse("password_reset"), {'email': user_email})
    assert response.status_code == 302
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_edit_account_view_get_not_logged_in(user):
    client = Client()
    response = client.get(reverse("edit_user"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_account_view_get_logged_in(user):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("edit_user"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_account_view_post_logged_in(user):
    client = Client()
    client.force_login(user[0])
    user = user[0]
    old_username = user.username
    old_email = user.email
    new_user_data = {
        'username': faker.first_name(),
        'email': faker.email(),
    }
    response = client.post(reverse("edit_user"), data=new_user_data)
    user.refresh_from_db()
    new_username = user.username
    new_email = user.email
    assert response.status_code == 302
    assert old_username != new_username
    assert old_email != new_email


@pytest.mark.django_db
def test_edit_account_view_post_not_logged_in(user):
    client = Client()
    user = user[0]
    old_username = user.username
    old_email = user.email
    new_user_data = {
        'username': faker.first_name(),
        'email': faker.email(),
    }
    response = client.post(reverse("edit_user"), data=new_user_data)
    user.refresh_from_db()
    new_username = user.username
    new_email = user.email
    assert response.status_code == 302
    assert old_username == new_username
    assert old_email == new_email


@pytest.mark.django_db
def test_edit_account_view_post_not_logged_in(user):
    client = Client()
    new_user_data = {
        'username': faker.first_name(),
        'email': faker.email(),
    }
    response = client.post(reverse("edit_user"), data=new_user_data)
    assert response.status_code == 302




@pytest.mark.django_db
def test_main_page_view_get_not_logged_in():
    client = Client()
    response = client.get(reverse("main-page"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_main_page_view_get_logged_in(user):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("main-page"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_project_view_get_logged_in(user):
    client = Client()
    client.force_login(user[0])
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
    client.force_login(user[0])
    project = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'user': user
    }
    old_projects_count = Project.objects.filter(user=user[0]).count()
    response = client.post(reverse("create-project-view"), data=project)
    assert response.status_code == 302
    new_projects_count = Project.objects.filter(user=user[0])
    assert old_projects_count + 1 == new_projects_count.count()


@pytest.mark.django_db
def test_create_project_view_post_not_logged_in(user, projects):
    client = Client()
    project = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'user': user
    }
    old_projects_count = Project.objects.filter(user=user[0]).count()
    response = client.post(reverse("create-project-view"), data=project)
    assert response.status_code == 302
    new_projects_count = Project.objects.filter(user=user[0])
    assert old_projects_count == new_projects_count.count()


@pytest.mark.django_db
def test_create_project_modal_view_get_logged_in(user):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("create_project_bs"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_project_modal_view_get_not_logged_in(user):
    client = Client()
    response = client.get(reverse("create_project_bs"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_project_modal_view_post_logged_in(user, projects):
    client = Client()
    client.force_login(user[0])
    project = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'user': user
    }
    old_projects_count = Project.objects.filter(user=user[0]).count()
    response = client.post(reverse("create_project_bs"), data=project)
    assert response.status_code == 302
    new_projects_count = Project.objects.filter(user=user[0])
    assert old_projects_count + 1 == new_projects_count.count()


@pytest.mark.django_db
def test_create_project_modal_view_post_not_logged_in(user, projects):
    client = Client()
    project = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'user': user
    }
    old_projects_count = Project.objects.filter(user=user[0]).count()
    response = client.post(reverse("create_project_bs"), data=project)
    assert response.status_code == 302
    new_projects_count = Project.objects.filter(user=user[0])
    assert old_projects_count == new_projects_count.count()


@pytest.mark.django_db
def test_delete_project_view_get_correct_user_logged_in(user, projects):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("delete_project_view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_project_view_get_wrong_user_logged_in(user, projects):
    client = Client()
    client.force_login(user[1])
    response = client.get(reverse("delete_project_view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_project_view_get_not_logged_in(user, projects):
    client = Client()
    response = client.get(reverse("delete_project_view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_project_view_post_correct_user_logged_in(user, projects):
    client = Client()
    client.force_login(user[0])
    old_project_count = len(projects)
    response = client.post(reverse("delete_project_view", kwargs={'pk': projects[0].pk}))
    new_project_count = [project for project in Project.objects.all()]
    assert response.status_code == 302
    assert old_project_count == len(new_project_count) + 1


@pytest.mark.django_db
def test_delete_project_view_post_wrong_user_logged_in(user, projects):
    client = Client()
    client.force_login(user[1])
    old_project_count = len(projects)
    response = client.post(reverse("delete_project_view", kwargs={'pk': projects[0].pk}))
    new_project_count = [project for project in Project.objects.all()]
    assert response.status_code == 404
    assert old_project_count == len(new_project_count)


@pytest.mark.django_db
def test_delete_project_view_post_not_logged_in(user, projects):
    client = Client()
    old_project_count = len(projects)
    response = client.post(reverse("delete_project_view", kwargs={'pk': projects[0].pk}))
    new_project_count = [project for project in Project.objects.all()]
    assert response.status_code == 302
    assert old_project_count == len(new_project_count)


@pytest.mark.django_db
def test_update_project_view_get_correct_user_logged_in(user, projects):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("update_project_view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_project_view_get_wrong_user_logged_in(user, projects):
    client = Client()
    client.force_login(user[1])
    response = client.get(reverse("update_project_view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_project_view_get_not_logged_in(user, projects):
    client = Client()
    response = client.get(reverse("update_project_view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_project_view_post_correct_user_logged_in(user, projects):
    client = Client()
    client.force_login(user[0])
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
def test_update_project_view_post_wrong_user_logged_in(user, projects):
    client = Client()
    client.force_login(user[1])
    project = projects[0]
    old_name = project.name
    old_description = project.description
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    response = client.post(reverse('update_project_view', kwargs={'pk': project.pk}),
                           {'name': new_name, 'description': new_description})
    assert response.status_code == 404
    project.refresh_from_db()
    assert project.name == old_name
    assert project.description == old_description


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
    client.force_login(user[0])
    response = client.get(reverse("subprojects-view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 200
    subprojects_list = response.context['object_list']
    target_subprojects = SubProject.objects.filter(parent=projects[0])
    assert subprojects_list.count() == target_subprojects.count()


@pytest.mark.django_db
def test_create_subproject_view_get_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[0])
    project = projects[0]
    response = client.get(reverse("create-subproject-view", kwargs={'pk': project.pk}))
    assert response.status_code == 200
    assert response.context['form']


@pytest.mark.django_db
def test_create_subproject_view_get_not_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    project = projects[0]
    response = client.get(reverse("create-subproject-view", kwargs={'pk': project.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_subproject_view_post_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[0])
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
def test_delete_subproject_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[0])
    project = projects[0]
    response = client.get(reverse("delete_subproject_view", kwargs={'pk': project.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_subproject_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[1])
    project = projects[0]
    response = client.get(reverse("delete_subproject_view", kwargs={'pk': project.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_subproject_view_get_not_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    project = projects[0]
    response = client.get(reverse("delete_subproject_view", kwargs={'pk': project.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_subproject_view_post_correct_user_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[0])
    old_subproject_count = len(subprojects)
    response = client.post(reverse("delete_subproject_view", kwargs={'pk': subprojects[0].pk}))
    new_subproject_count = SubProject.objects.all().count()
    assert response.status_code == 302
    assert old_subproject_count == new_subproject_count + 1


@pytest.mark.django_db
def test_delete_subproject_view_post_wrong_user_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[1])
    old_subproject_count = len(subprojects)
    response = client.post(reverse("delete_subproject_view", kwargs={'pk': subprojects[0].pk}))
    new_subproject_count = SubProject.objects.all().count()
    assert response.status_code == 404
    assert old_subproject_count == new_subproject_count


@pytest.mark.django_db
def test_delete_subproject_view_post_not_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    old_subproject_count = len(subprojects)
    response = client.post(reverse("delete_subproject_view", kwargs={'pk': subprojects[0].pk}))
    new_subproject_count = SubProject.objects.all().count()
    assert response.status_code == 302
    assert old_subproject_count == new_subproject_count


@pytest.mark.django_db
def test_update_subproject_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[0])
    subproject = subprojects[0]
    response = client.get(reverse("update_subproject_view", kwargs={'pk': subproject.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_subproject_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[1])
    subproject = subprojects[0]
    response = client.get(reverse("update_subproject_view", kwargs={'pk': subproject.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_subproject_view_get_not_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    subproject = subprojects[0]
    response = client.get(reverse("update_subproject_view", kwargs={'pk': subproject.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_subproject_view_post_correct_user_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[0])
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
def test_update_subproject_view_post_wrong_user_logged_in(user, projects, terms, crew_members, subprojects):
    client = Client()
    client.force_login(user[1])
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
    assert response.status_code == 404
    subproject.refresh_from_db()
    assert subproject.name == old_name
    assert subproject.description == old_description


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
def test_subproject_detail_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    selected_subproject = subprojects[0]
    response = client.get(reverse("subproject_detail_view", kwargs={'pk': selected_subproject.pk}))
    assert response.status_code == 200
    assert response.context['object']
    subproject_detail_data = response.context['object']
    assert subproject_detail_data.name
    assert subproject_detail_data.parent


@pytest.mark.django_db
def test_subproject_detail_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[1])
    selected_subproject = subprojects[0]
    response = client.get(reverse("subproject_detail_view", kwargs={'pk': selected_subproject.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_shooting_days_view_get_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    response = client.get(reverse("shooting-days-view", kwargs={'pk': subprojects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_shooting_days_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("shooting-days-view", kwargs={'pk': subprojects[0].pk}))
    assert response.status_code == 200
    shooting_days_list = response.context['object_list']
    target_shooting_days = ShootingDay.objects.filter(subproject=subprojects[0])
    assert shooting_days_list.count() == target_shooting_days.count()


@pytest.mark.django_db
def test_create_shooting_day_view_post_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
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
def test_delete_shooting_day_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                             shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("delete_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_shooting_day_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                           shooting_days):
    client = Client()
    client.force_login(user[1])
    response = client.get(reverse("delete_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_shooting_day_view_get_not_logged_in(user, projects, terms, crew_members, subprojects,
                                                    shooting_days):
    client = Client()
    response = client.get(reverse("delete_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_shooting_day_view_post_correct_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    old_shooting_days_count = len(shooting_days)
    response = client.post(reverse("delete_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    new_shooting_days_count = ShootingDay.objects.all().count()
    assert response.status_code == 302
    assert old_shooting_days_count == new_shooting_days_count + 1


@pytest.mark.django_db
def test_delete_shooting_day_view_post_wrong_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[1])
    old_shooting_days_count = len(shooting_days)
    response = client.post(reverse("delete_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    new_shooting_days_count = ShootingDay.objects.all().count()
    assert response.status_code == 404
    assert old_shooting_days_count == new_shooting_days_count


@pytest.mark.django_db
def test_delete_shooting_day_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    old_shooting_days_count = len(shooting_days)
    response = client.post(reverse("delete_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    new_shooting_days_count = ShootingDay.objects.all().count()
    assert response.status_code == 302
    assert old_shooting_days_count == new_shooting_days_count


@pytest.mark.django_db
def test_update_shooting_day_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                             shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("update_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_shooting_day_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                             shooting_days):
    client = Client()
    client.force_login(user[1])
    response = client.get(reverse("update_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_shooting_day_view_get_not_logged_in(user, projects, terms, crew_members, subprojects,
                                                             shooting_days):
    client = Client()
    response = client.get(reverse("update_shootingday_view", kwargs={'pk': shooting_days[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_shooting_day_view_post_correct_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
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
def test_update_shooting_day_view_post_wrong_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[1])
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
    assert response.status_code == 404
    shooting_day.refresh_from_db()
    assert shooting_day.name == old_name
    assert shooting_day.description == old_description


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
def test_shooting_day_detail_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    shooting_day = shooting_days[0]
    response = client.get(reverse("shootingday_detail_view", kwargs={'pk': shooting_day.pk}))
    assert response.status_code == 200
    assert response.context['object']
    shooting_day_data = response.context['object']
    assert shooting_day_data.name
    assert shooting_day_data.date


@pytest.mark.django_db
def test_shooting_day_detail_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[1])
    shooting_day = shooting_days[0]
    response = client.get(reverse("shootingday_detail_view", kwargs={'pk': shooting_day.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_shooting_day_detail_view_get_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    shooting_day = shooting_days[0]
    response = client.get(reverse("shootingday_detail_view", kwargs={'pk': shooting_day.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_terms_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("create_terms", kwargs={'pk': subprojects[0].pk}))
    assert response.status_code == 200
    assert response.context.get('form')


@pytest.mark.django_db
def test_create_terms_view_get_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    response = client.get(reverse("create_terms", kwargs={'pk': subprojects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_terms_view_post_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    new_terms_data = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'pay_period': 1,
        'base_rate': 1500,
        'ot_rate': 35,
        'camera_ot_rate': 50,
        'extras': 0,
        'user': user[0],
        'working_hours': 1,
    }
    old_terms_count = Terms.objects.all().count()
    response = client.post(reverse("create_terms", kwargs={'pk': projects[0].pk}), data=new_terms_data)
    assert response.status_code == 302
    new_terms_count = Terms.objects.all()
    assert old_terms_count + 1 == new_terms_count.count()


@pytest.mark.django_db
def test_create_terms_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    new_terms_data = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'pay_period': 1,
        'base_rate': 1500,
        'ot_rate': 35,
        'camera_ot_rate': 50,
        'extras': 0,
        'user': user[0],
        'working_hours': 1,
    }
    old_terms_count = Terms.objects.all().count()
    response = client.post(reverse("create_terms", kwargs={'pk': projects[0].pk}), data=new_terms_data)
    assert response.status_code == 302
    new_terms_count = Terms.objects.all()
    assert old_terms_count == new_terms_count.count()


@pytest.mark.django_db
def test_create_terms_modal_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("create_terms_bs"))
    assert response.status_code == 200
    assert response.context.get('form')


@pytest.mark.django_db
def test_create_terms_modal_view_get_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    response = client.get(reverse("create_terms_bs"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_terms_modal_view_post_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    new_terms_data = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'pay_period': 1,
        'base_rate': 1500,
        'ot_rate': 35,
        'camera_ot_rate': 50,
        'extras': 0,
        'user': user[0],
        'working_hours': 1,
    }
    old_terms_count = Terms.objects.all().count()
    response = client.post(reverse("create_terms_bs"), data=new_terms_data)
    assert response.status_code == 302
    new_terms_count = Terms.objects.all()
    assert old_terms_count + 1 == new_terms_count.count()


@pytest.mark.django_db
def test_create_terms_modal_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    new_terms_data = {
        'name': faker.text(max_nb_chars=20),
        'description': faker.text(max_nb_chars=20),
        'pay_period': 1,
        'base_rate': 1500,
        'ot_rate': 35,
        'camera_ot_rate': 50,
        'extras': 0,
        'user': user[0],
        'working_hours': 1,
    }
    old_terms_count = Terms.objects.all().count()
    response = client.post(reverse("create_terms_bs"), data=new_terms_data)
    assert response.status_code == 302
    new_terms_count = Terms.objects.all()
    assert old_terms_count == new_terms_count.count()


@pytest.mark.django_db
def test_terms_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("terms-view", kwargs={'pk': subprojects[0].pk}))
    assert response.status_code == 200
    terms_list = response.context['object_list']
    target_terms = Terms.objects.filter(user=user[0])
    assert terms_list.count() == target_terms.count()


@pytest.mark.django_db
def test_terms_view_get_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    response = client.get(reverse("terms-view", kwargs={'pk': subprojects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_terms_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                      shooting_days):
    client = Client()
    client.force_login(user[0])
    selected_terms = terms[0]
    response = client.get(reverse("delete_terms", kwargs={'pk': selected_terms.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_terms_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                      shooting_days):
    client = Client()
    client.force_login(user[1])
    selected_terms = terms[0]
    response = client.get(reverse("delete_terms", kwargs={'pk': selected_terms.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_terms_view_get_not_logged_in(user, projects, terms, crew_members, subprojects,
                                             shooting_days):
    client = Client()
    selected_terms = terms[0]
    response = client.get(reverse("delete_terms", kwargs={'pk': selected_terms.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_terms_view_post_correct_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    selected_terms = terms[0]
    old_terms_count = Terms.objects.all().count()
    response = client.post(reverse("delete_terms", kwargs={'pk': selected_terms.pk}))
    new_terms_count = Terms.objects.all().count()
    assert response.status_code == 302
    assert old_terms_count == new_terms_count + 1


@pytest.mark.django_db
def test_delete_terms_view_post_wrong_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[1])
    selected_terms = terms[0]
    old_terms_count = Terms.objects.all().count()
    response = client.post(reverse("delete_terms", kwargs={'pk': selected_terms.pk}))
    new_terms_count = Terms.objects.all().count()
    assert response.status_code == 404
    assert old_terms_count == new_terms_count



@pytest.mark.django_db
def test_delete_terms_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    selected_terms = terms[0]
    old_terms_count = Terms.objects.all().count()
    response = client.post(reverse("delete_terms", kwargs={'pk': selected_terms.pk}))
    new_terms_count = Terms.objects.all().count()
    assert response.status_code == 302
    assert old_terms_count == new_terms_count


@pytest.mark.django_db
def test_update_terms_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                      shooting_days):
    client = Client()
    client.force_login(user[0])
    selected_terms = terms[0]
    response = client.get(reverse("update_terms", kwargs={'pk': selected_terms.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_terms_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                    shooting_days):
    client = Client()
    client.force_login(user[1])
    selected_terms = terms[0]
    response = client.get(reverse("update_terms", kwargs={'pk': selected_terms.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_terms_view_get_not_logged_in(user, projects, terms, crew_members, subprojects,
                                                    shooting_days):
    client = Client()
    selected_terms = terms[0]
    response = client.get(reverse("update_terms", kwargs={'pk': selected_terms.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_terms_view_post_correct_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    selected_terms = terms[0]
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    new_terms_data = {
        'name': new_name,
        'description': new_description,
        'pay_period': selected_terms.pay_period,
        'base_rate': selected_terms.base_rate,
        'ot_rate': selected_terms.ot_rate,
        'camera_ot_rate': selected_terms.camera_ot_rate,
        'extras': selected_terms.extras,
        'working_hours': selected_terms.working_hours,
        'user': selected_terms.user,
    }
    response = client.post(reverse('update_terms', kwargs={'pk': selected_terms.pk}),
                           data=new_terms_data)
    assert response.status_code == 302
    selected_terms.refresh_from_db()
    assert selected_terms.name == new_name
    assert selected_terms.description == new_description


@pytest.mark.django_db
def test_update_terms_view_post_wrong_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[1])
    selected_terms = terms[0]
    old_name = selected_terms.name
    old_description = selected_terms.description
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    new_terms_data = {
        'name': new_name,
        'description': new_description,
        'pay_period': selected_terms.pay_period,
        'base_rate': selected_terms.base_rate,
        'ot_rate': selected_terms.ot_rate,
        'camera_ot_rate': selected_terms.camera_ot_rate,
        'extras': selected_terms.extras,
        'working_hours': selected_terms.working_hours,
        'user': selected_terms.user,
    }
    response = client.post(reverse('update_terms', kwargs={'pk': selected_terms.pk}),
                           data=new_terms_data)
    assert response.status_code == 404
    selected_terms.refresh_from_db()
    assert selected_terms.name == old_name
    assert selected_terms.description == old_description


@pytest.mark.django_db
def test_update_terms_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    selected_terms = terms[0]
    old_name = selected_terms.name
    old_description = selected_terms.description
    new_name = faker.text(max_nb_chars=20)
    new_description = faker.text(max_nb_chars=20)
    new_terms_data = {
        'name': new_name,
        'description': new_description,
        'pay_period': selected_terms.pay_period,
        'base_rate': selected_terms.base_rate,
        'ot_rate': selected_terms.ot_rate,
        'camera_ot_rate': selected_terms.camera_ot_rate,
        'extras': selected_terms.extras,
        'working_hours': selected_terms.working_hours,
        'user': selected_terms.user,
    }
    response = client.post(reverse('update_terms', kwargs={'pk': selected_terms.pk}),
                           data=new_terms_data)
    assert response.status_code == 302
    selected_terms.refresh_from_db()
    assert selected_terms.name == old_name
    assert selected_terms.description == old_description


@pytest.mark.django_db
def test_crew_members_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("crew-members-view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 200
    crew_members_list = response.context['object_list']
    target_crew_members = CrewMember.objects.filter(user=user[0])
    assert crew_members_list.count() == target_crew_members.count()


@pytest.mark.django_db
def test_crew_members_view_get_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    response = client.get(reverse("crew-members-view", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_crew_members_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("create_crew_member", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_crew_members_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    response = client.get(reverse("create_crew_member", kwargs={'pk': projects[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_crew_members_view_post_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    new_crew_member_data = {
        'name': faker.first_name(),
        'surname': faker.last_name(),
        'contact_info': faker.text(max_nb_chars=10),
        'position': faker.text(max_nb_chars=10),
        'user': user[0],
    }
    old_crew_members_count = CrewMember.objects.all().count()
    response = client.post(reverse("create_crew_member", kwargs={'pk': projects[0].pk}), data=new_crew_member_data)
    assert response.status_code == 302
    new_crew_members_count = CrewMember.objects.all().count()
    assert old_crew_members_count + 1 == new_crew_members_count


@pytest.mark.django_db
def test_create_crew_members_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    new_crew_member_data = {
        'name': faker.first_name(),
        'surname': faker.last_name(),
        'contact_info': faker.text(max_nb_chars=10),
        'position': faker.text(max_nb_chars=10),
        'user': user[0],
    }
    old_crew_members_count = CrewMember.objects.all().count()
    response = client.post(reverse("create_crew_member", kwargs={'pk': projects[0].pk}), data=new_crew_member_data)
    assert response.status_code == 302
    new_crew_members_count = CrewMember.objects.all().count()
    assert old_crew_members_count == new_crew_members_count


@pytest.mark.django_db
def test_create_crew_members_modal_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    response = client.get(reverse("create_crew_member_bs"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_crew_members_modal_view_get_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    response = client.get(reverse("create_crew_member_bs"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_crew_members_modal_view_post_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    new_crew_member_data = {
        'name': faker.first_name(),
        'surname': faker.last_name(),
        'contact_info': faker.text(max_nb_chars=10),
        'position': faker.text(max_nb_chars=10),
        'user': user[0],
    }
    old_crew_members_count = CrewMember.objects.all().count()
    response = client.post(reverse("create_crew_member_bs"), data=new_crew_member_data)
    assert response.status_code == 302
    new_crew_members_count = CrewMember.objects.all().count()
    assert old_crew_members_count + 1 == new_crew_members_count


@pytest.mark.django_db
def test_create_crew_members_modal_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    new_crew_member_data = {
        'name': faker.first_name(),
        'surname': faker.last_name(),
        'contact_info': faker.text(max_nb_chars=10),
        'position': faker.text(max_nb_chars=10),
        'user': user[0],
    }
    old_crew_members_count = CrewMember.objects.all().count()
    response = client.post(reverse("create_crew_member_bs"), data=new_crew_member_data)
    assert response.status_code == 302
    new_crew_members_count = CrewMember.objects.all().count()
    assert old_crew_members_count == new_crew_members_count



@pytest.mark.django_db
def test_update_crew_members_view_get_correct_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                             shooting_days):
    client = Client()
    client.force_login(user[0])
    selected_crew_member = crew_members[0]
    response = client.get(reverse("update_crew_member", kwargs={'pk': selected_crew_member.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_crew_members_view_get_wrong_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                           shooting_days):
    client = Client()
    client.force_login(user[1])
    selected_crew_member = crew_members[0]
    response = client.get(reverse("update_crew_member", kwargs={'pk': selected_crew_member.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_crew_members_view_get_not_logged_in(user, projects, terms, crew_members, subprojects,
                                                    shooting_days):
    client = Client()
    selected_crew_member = crew_members[0]
    response = client.get(reverse("update_crew_member", kwargs={'pk': selected_crew_member.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_crew_members_view_post_correct_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    selected_crew_member = crew_members[0]
    new_name = faker.first_name()
    new_surname = faker.last_name()
    new_crew_member_data = {
        'name': new_name,
        'surname': new_surname,
        'contact_info': selected_crew_member.contact_info,
        'position': selected_crew_member.position,
        'user': selected_crew_member.user
    }
    response = client.post(reverse('update_crew_member', kwargs={'pk': selected_crew_member.pk}),
                           data=new_crew_member_data)
    assert response.status_code == 302
    selected_crew_member.refresh_from_db()
    assert selected_crew_member.name == new_name
    assert selected_crew_member.surname == new_surname


@pytest.mark.django_db
def test_update_crew_members_view_post_wrong_user_logged_in(user, projects, terms, crew_members, subprojects,
                                                            shooting_days):
    client = Client()
    client.force_login(user[1])
    selected_crew_member = crew_members[0]
    old_name = selected_crew_member.name
    old_surname = selected_crew_member.surname
    new_name = faker.first_name()
    new_surname = faker.last_name()
    new_crew_member_data = {
        'name': new_name,
        'surname': new_surname,
        'contact_info': selected_crew_member.contact_info,
        'position': selected_crew_member.position,
        'user': selected_crew_member.user
    }
    response = client.post(reverse('update_crew_member', kwargs={'pk': selected_crew_member.pk}),
                           data=new_crew_member_data)
    assert response.status_code == 404
    selected_crew_member.refresh_from_db()
    assert selected_crew_member.name == old_name
    assert selected_crew_member.surname == old_surname


@pytest.mark.django_db
def test_update_crew_members_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    selected_crew_member = crew_members[0]
    old_name = selected_crew_member.name
    old_surname = selected_crew_member.surname
    new_name = faker.first_name()
    new_surname = faker.last_name()
    new_crew_member_data = {
        'name': new_name,
        'surname': new_surname,
        'contact_info': selected_crew_member.contact_info,
        'position': selected_crew_member.position,
        'user': selected_crew_member.user
    }
    response = client.post(reverse('update_crew_member', kwargs={'pk': selected_crew_member.pk}),
                           data=new_crew_member_data)
    assert response.status_code == 302
    selected_crew_member.refresh_from_db()
    assert selected_crew_member.name == old_name
    assert selected_crew_member.surname == old_surname


@pytest.mark.django_db
def test_delete_crew_member_view_post_correct_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[0])
    selected_crew_member = crew_members[0]
    old_crew_members_count = CrewMember.objects.all().count()
    response = client.post(reverse("delete_crew_member", kwargs={'pk': selected_crew_member.pk}))
    new_crew_members_count = CrewMember.objects.all().count()
    assert response.status_code == 302
    assert old_crew_members_count == new_crew_members_count + 1


@pytest.mark.django_db
def test_delete_crew_member_view_post_wrong_user_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    client.force_login(user[1])
    selected_crew_member = crew_members[0]
    old_crew_members_count = CrewMember.objects.all().count()
    response = client.post(reverse("delete_crew_member", kwargs={'pk': selected_crew_member.pk}))
    new_crew_members_count = CrewMember.objects.all().count()
    assert response.status_code == 404
    assert old_crew_members_count == new_crew_members_count


@pytest.mark.django_db
def test_delete_crew_member_view_post_not_logged_in(user, projects, terms, crew_members, subprojects, shooting_days):
    client = Client()
    selected_crew_member = crew_members[0]
    old_crew_members_count = CrewMember.objects.all().count()
    response = client.post(reverse("delete_crew_member", kwargs={'pk': selected_crew_member.pk}))
    new_crew_members_count = CrewMember.objects.all().count()
    assert response.status_code == 302
    assert old_crew_members_count == new_crew_members_count
