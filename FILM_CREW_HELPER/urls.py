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
    ProjectCreateViewBS, DeleteProjectView, DeleteSubProjectView, TermsCreateViewBS, CrewMemberCreateViewBS, \
    ShootingDaysView, CreateShootingDayView, UpdateProjectView, UpdateSubProjectView, TermsCreateView, \
    DeleteShootingDayView, UpdateShootingDayView, ShootingDayDetailView, AboutView, ContactView, TermsView, \
    DeleteTermsView, UpdateTermsView, CrewMembersView, CrewMemberCreateView, UpdateCrewMemberView, DeleteCrewMemberView, \
    SubProjectDetailView, check_toc


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index-view'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('main/', MainPageView.as_view(), name='main-page'),
    path('about/', AboutView.as_view(), name='about-page'),
    path('contact/', ContactView.as_view(), name='contact-page'),
    path('subprojects/<int:pk>/', SubProjectsView.as_view(), name='subprojects-view'),
    path('create_project/', CreateProjectView.as_view(), name='create-project-view'),
    path('create_subproject/<int:pk>/', CreateSubProjectView.as_view(), name='create-subproject-view'),
    path('create_project_bs/', ProjectCreateViewBS.as_view(), name='create_project_bs'),
    path('delete_project/<int:pk>/', DeleteProjectView.as_view(), name='delete_project_view'),
    path('update_project/<int:pk>/', UpdateProjectView.as_view(), name='update_project_view'),
    path('delete_subproject/<int:pk>/', DeleteSubProjectView.as_view(), name='delete_subproject_view'),
    path('update_subproject/<int:pk>/', UpdateSubProjectView.as_view(), name='update_subproject_view'),
    path('subproject/<int:pk>/', SubProjectDetailView.as_view(), name='subproject_detail_view'),
    path('create_terms_bs/', TermsCreateViewBS.as_view(), name='create_terms_bs'),
    path('create_terms/<int:pk>/', TermsCreateView.as_view(), name='create_terms'),
    path('delete_terms/<int:pk>/', DeleteTermsView.as_view(), name='delete_terms'),
    path('update_terms/<int:pk>/', UpdateTermsView.as_view(), name='update_terms'),
    path('terms/<int:pk>/', TermsView.as_view(), name='terms-view'),
    path('create_crew_member_bs/', CrewMemberCreateViewBS.as_view(), name='create_crew_member_bs'),
    path('shooting_days/<int:pk>/', ShootingDaysView.as_view(), name='shooting-days-view'),
    path('create_shootingday/<int:pk>/', CreateShootingDayView.as_view(), name='create-shootingday-view'),
    path('check_toc', check_toc, name='check_toc'),
    path('delete_shootingday/<int:pk>/', DeleteShootingDayView.as_view(), name='delete_shootingday_view'),
    path('update_shootingday/<int:pk>/', UpdateShootingDayView.as_view(), name='update_shootingday_view'),
    path('shootingday/<int:pk>/', ShootingDayDetailView.as_view(), name='shootingday_detail_view'),
    path('crew_members/<int:pk>/', CrewMembersView.as_view(), name='crew-members-view'),
    path('create_crew_members/<int:pk>/', CrewMemberCreateView.as_view(), name='create_crew_member'),
    path('update_crew_members/<int:pk>/', UpdateCrewMemberView.as_view(), name='update_crew_member'),
    path('delete_crew_members/<int:pk>/', DeleteCrewMemberView.as_view(), name='delete_crew_member'),

]
