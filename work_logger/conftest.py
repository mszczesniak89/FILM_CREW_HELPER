import random
from datetime import timedelta

import pytest
from django.contrib.auth.models import User, Permission
from accounts.models import CustomUser
from work_logger.models import Project, SubProject, ShootingDay, Terms, CrewMember
from faker import Faker
faker = Faker("pl_PL")

@pytest.fixture
def user():
    u = CustomUser.objects.create(username='testowy', id=1)
    return u


@pytest.fixture
def projects(user):
    lst = []
    for x in range(10):
        lst.append(Project.objects.create(name=faker.text(max_nb_chars=20), description=faker.text(max_nb_chars=20),
                                          user=user))
    return lst


@pytest.fixture
def terms(user):
    lst = []
    for x in range(5):
        lst.append(Terms.objects.create(name=faker.text(max_nb_chars=20), description=faker.text(max_nb_chars=20),
                                        user=user, pay_period=1, base_rate=400, ot_rate=35,
                                        camera_ot_rate=50, extras=0, working_hours=1))
    return lst


@pytest.fixture
def crew_members(user):
    lst = []
    for x in range(5):
        lst.append(CrewMember.objects.create(name=faker.first_name(), surname=faker.last_name(),
                                             position=faker.text(max_nb_chars=20),
                                             contact_info=faker.text(max_nb_chars=20), user=user))
    return lst


@pytest.fixture
def subprojects(projects, terms, crew_members):
    lst = []
    for x in range(10):
        subproject = SubProject.objects.create(parent=Project.objects.get(id=projects[0].pk),
                                               description=faker.text(max_nb_chars=20),
                                               name=faker.text(max_nb_chars=20), position=faker.text(max_nb_chars=10),
                                               terms=terms[0])
        subproject_diff_project = SubProject.objects.create(parent=Project.objects.get(id=projects[1].pk),
                                                            description=faker.text(max_nb_chars=20),
                                                            name=faker.text(max_nb_chars=20),
                                                            position=faker.text(max_nb_chars=20), terms=terms[0])
        crew_member = crew_members[0]
        subproject.crew_members.add(crew_member)
        subproject_diff_project.crew_members.add(crew_member)
        lst.append(subproject)
        lst.append(subproject_diff_project)
    return lst


@pytest.fixture
def shooting_days(user, subprojects):
    lst = []
    for x in range(5):
        random_date = faker.date_time_this_month()
        end_hour_shift = random_date + timedelta(hours=7)
        lst.append(ShootingDay.objects.create(name=faker.text(max_nb_chars=20), date=random_date,
                                              description=faker.text(max_nb_chars=20), start_hour=random_date,
                                              end_hour=end_hour_shift, ot=random.randint(0, 4),
                                              camera_ot=random.randint(0, 3), toc=0, extras=0,
                                              subproject=subprojects[0]))
    for x in range(5):
        random_date = faker.date_time_this_month()
        end_hour_shift = random_date + timedelta(hours=7)
        lst.append(ShootingDay.objects.create(name=faker.text(max_nb_chars=20), date=random_date,
                                              description=faker.text(max_nb_chars=20), start_hour=random_date,
                                              end_hour=end_hour_shift, ot=random.randint(0, 4),
                                              camera_ot=random.randint(0, 3), toc=0, extras=0,
                                              subproject=subprojects[1]))
    return lst
