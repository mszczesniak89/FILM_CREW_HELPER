"""FILM_CREW_HELPER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from work_logger.views import IndexView, MainPageView, SubProjectsView, CreateProjectView, CreateSubProjectView, \
    ProjectCreateViewBS, DeleteProjectView, DeleteSubProjectView, TermsCreateViewBS, CrewMemberCreateViewBS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index-view'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('main/', MainPageView.as_view(), name='main-page'),
    path('subprojects/<int:pk>/', SubProjectsView.as_view(), name='subprojects-view'),
    path('create_project/', CreateProjectView.as_view(), name='create-project-view'),
    path('create_subproject/', CreateSubProjectView.as_view(), name='create-subproject-view'),
    path('create_project_bs/', ProjectCreateViewBS.as_view(), name='create_project_bs'),
    path('delete_project/<int:pk>/', DeleteProjectView.as_view(), name='delete_project_view'),
    path('delete_subproject/<int:pk>/', DeleteSubProjectView.as_view(), name='delete_subproject_view'),
    path('create_terms_bs/', TermsCreateViewBS.as_view(), name='create_terms_bs'),
    path('create_crew_member_bs/', CrewMemberCreateViewBS.as_view(), name='create_crew_member_bs'),
]
