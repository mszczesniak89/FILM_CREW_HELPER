
import pytest
from django.contrib.auth.models import User, Permission
from accounts.models import CustomUser
from work_logger.models import Project, SubProject, ShootingDay, Terms, CrewMember


@pytest.fixture
def user():
    u = CustomUser.objects.create(username='testowy', id=1)
    return u


@pytest.fixture
def projects(user):
    lst = []
    for x in range(10):
        lst.append(Project.objects.create(name=x, description=x, user=user))
    return lst


@pytest.fixture
def terms(user):
    lst = []
    for x in range(2):
        lst.append(Terms.objects.create(name=x, description=x, user=user, pay_period=1, base_rate=400, ot_rate=35,
                                        camera_ot_rate=50, extras=0, working_hours=1))
    return lst


@pytest.fixture
def crew_members(user):
    lst = []
    for x in range(5):
        lst.append(CrewMember.objects.create(name=x, surname=x, position=x, contact_info=x, user=user))
    return lst


@pytest.fixture
def subprojects(projects, terms, crew_members):
    lst = []
    for x in range(10):
        subproject = SubProject.objects.create(parent=Project.objects.get(id=projects[0].pk),
                                               description=x, name=x, position=x, terms=terms[0])
        subproject_diff_project = SubProject.objects.create(parent=Project.objects.get(id=projects[1].pk),
                                                            description=x, name=x, position=x, terms=terms[0])
        crew_member = crew_members[0]
        subproject.crew_members.add(crew_member)
        subproject_diff_project.crew_members.add(crew_member)
        lst.append(subproject)
        lst.append(subproject_diff_project)
    return lst
