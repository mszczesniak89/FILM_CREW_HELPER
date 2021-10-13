from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import request, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm
from work_logger.models import Project, SubProject
from work_logger.filters import ProjectFilter, SubProjectFilter
from work_logger.forms import ProjectCreateForm, SubProjectCreateForm, ProjectCreateFormBS, TermsCreateFormBS, \
    CrewMemberCreateFormBS
from django_filters.views import FilterView
from bootstrap_modal_forms.generic import BSModalCreateView

# Create your views here.


class IndexView(View):
    def get(self, request):
        response = render(request, 'work_logger/home_page.html', )
        return response


class MainPageView(LoginRequiredMixin, FilterView):
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    model = Project
    context_object_name = 'object_list'
    filterset_class = ProjectFilter
    template_name = 'work_logger/main.html'


class SubProjectsView(LoginRequiredMixin, FilterView):
    def get_queryset(self):
        return SubProject.objects.filter(parent=self.kwargs['pk'])
    model = SubProject
    context_object_name = 'object_list'
    filterset_class = SubProjectFilter
    template_name = 'work_logger/subprojects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['pk'])
        return context


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'work_logger/create_project.html'
    success_url = reverse_lazy('main-page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CreateSubProjectView(LoginRequiredMixin, CreateView):
    model = SubProject
    form_class = SubProjectCreateForm
    template_name = 'work_logger/create_subproject.html'
    # success_url = reverse_lazy('subprojects-view')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreateSubProjectView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy('subprojects-view', kwargs={'pk': self.object.parent.pk})


class ProjectCreateViewBS(BSModalCreateView):
    template_name = 'work_logger/create_project_bs.html'
    form_class = ProjectCreateFormBS
    success_message = 'Success: Project was created.'
    success_url = reverse_lazy('create-subproject-view')

    def form_valid(self, form):
        user = self.request.user
        f = form.save(commit=False)
        f.user = user
        return super().form_valid(form)


class DeleteProjectView(DeleteView):
    model = Project
    success_url = reverse_lazy('main-page')
    template_name = 'work_logger/delete_form.html'


class DeleteSubProjectView(DeleteView):
    model = SubProject
    template_name = 'work_logger/delete_form.html'

    def get_success_url(self):
        return reverse_lazy('subprojects-view', kwargs={'pk': self.object.parent.pk})


class TermsCreateViewBS(BSModalCreateView):
    template_name = 'work_logger/create_terms_bs.html'
    form_class = TermsCreateFormBS
    success_message = 'Success: Terms were created.'
    success_url = reverse_lazy('create-subproject-view')

    def form_valid(self, form):
        user = self.request.user
        f = form.save(commit=False)
        f.user = user
        return super().form_valid(form)


class CrewMemberCreateViewBS(BSModalCreateView):
    template_name = 'work_logger/create_crew_member_bs.html'
    form_class = CrewMemberCreateFormBS
    success_message = 'Success: Crew member was created.'
    success_url = reverse_lazy('create-subproject-view')

    def form_valid(self, form):
        user = self.request.user
        f = form.save(commit=False)
        f.user = user
        return super().form_valid(form)

