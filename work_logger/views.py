from braces.views import UserFormKwargsMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import request, HttpResponseRedirect, Http404, JsonResponse
import iso8601
from datetime import datetime, timedelta
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm
from work_logger.models import Project, SubProject, ShootingDay, Terms, CrewMember
from work_logger.filters import ProjectFilter, SubProjectFilter, ShootingDayFilter, TermsFilter, CrewMembersFilter
from work_logger.forms import ProjectCreateForm, SubProjectCreateForm, ProjectCreateFormBS, TermsCreateFormBS, \
    CrewMemberCreateFormBS, ShootingDayCreateForm, TermsCreateForm, CrewMemberCreateForm
from django_filters.views import FilterView
from bootstrap_modal_forms.generic import BSModalCreateView


class IndexView(View):
    def get(self, request):
        response = render(request, 'work_logger/home_page.html', )
        return response

    def post(self, request):
        response = render(request, 'work_logger/home_page.html', )
        return response


class AboutView(View):
    def get(self, request):
        response = render(request, 'work_logger/about.html', )
        return response

    def post(self, request):
        response = render(request, 'work_logger/about.html', )
        return response


class ContactView(View):
    def get(self, request):
        response = render(request, 'work_logger/contact.html', )
        return response

    def post(self, request):
        response = render(request, 'work_logger/contact.html', )
        return response


class MainPageView(LoginRequiredMixin, FilterView):
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    model = Project
    context_object_name = 'object_list'
    filterset_class = ProjectFilter
    template_name = 'work_logger/main.html'


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'work_logger/create_project.html'
    success_url = reverse_lazy('main-page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectCreateViewBS(LoginRequiredMixin, UserFormKwargsMixin, BSModalCreateView):
    template_name = 'work_logger/create_project_bs.html'
    form_class = ProjectCreateFormBS
    success_message = 'Success: Project was created.'

    def form_valid(self, form):
        if not self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('create-subproject-view', kwargs={'pk': self.object.pk})


class DeleteProjectView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('main-page')
    template_name = 'work_logger/delete_form.html'

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.user
        return logged_in_user == content_user


class UpdateProjectView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    success_url = reverse_lazy('main-page')
    template_name = 'work_logger/update_form.html'
    form_class = ProjectCreateForm

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.user
        return logged_in_user == content_user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = "PROJECT"
        return context


class SubProjectsView(LoginRequiredMixin, FilterView):
    def get_queryset(self):
        return SubProject.objects.filter(parent__user=self.request.user).filter(parent=self.kwargs['pk'])

    model = SubProject
    context_object_name = 'object_list'
    filterset_class = SubProjectFilter
    template_name = 'work_logger/subprojects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['pk'])
        return context


class CreateSubProjectView(LoginRequiredMixin, CreateView):
    model = SubProject
    form_class = SubProjectCreateForm
    template_name = 'work_logger/create_subproject.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreateSubProjectView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_initial(self):
        parent = Project.objects.get(id=self.kwargs['pk'])
        return {
            'parent': parent,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('subprojects-view', kwargs={'pk': self.object.parent.pk})


class DeleteSubProjectView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubProject
    template_name = 'work_logger/delete_form.html'

    def get_success_url(self):
        return reverse_lazy('subprojects-view', kwargs={'pk': self.object.parent.pk})

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.parent.user
        return logged_in_user == content_user


class UpdateSubProjectView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubProject
    template_name = 'work_logger/update_form.html'
    form_class = SubProjectCreateForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UpdateSubProjectView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = "SUB-PROJECT"
        return context

    def get_success_url(self):
        return reverse_lazy('subprojects-view', kwargs={'pk': self.object.parent.pk})

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.parent.user
        return logged_in_user == content_user


class SubProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = SubProject
    template_name = 'work_logger/subproject_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = "SUB-PROJECT"
        return context

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.parent.user
        return logged_in_user == content_user


class ShootingDaysView(LoginRequiredMixin, FilterView):
    def get_queryset(self):
        user = self.request.user
        return ShootingDay.objects.filter(subproject__parent__user=user).filter(subproject=self.kwargs['pk'])

    model = ShootingDay
    context_object_name = 'object_list'
    filterset_class = ShootingDayFilter
    template_name = 'work_logger/shooting_days.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subproject'] = SubProject.objects.get(id=self.kwargs['pk'])
        if ShootingDay.objects.filter(subproject=self.kwargs['pk']).count() > 0:
            context['stats_days'] = ShootingDay.objects.filter(subproject=self.kwargs['pk']).count()
            stats_total_hours_worked = 0
            for day in ShootingDay.objects.filter(subproject=self.kwargs['pk']):
                diff = day.end_hour - day.start_hour
                diff_in_hours = diff.total_seconds() / 3600
                stats_total_hours_worked += diff_in_hours
            context['stats_total_hours_worked'] = round(stats_total_hours_worked, 1)
            context['stats_avr_hours_per_day'] = round(round(stats_total_hours_worked, 1) / ShootingDay.objects.filter(
                subproject=self.kwargs['pk']).count(), 1)
        return context


class CreateShootingDayView(LoginRequiredMixin, CreateView):
    model = ShootingDay
    form_class = ShootingDayCreateForm
    template_name = 'work_logger/create_shootingday.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreateShootingDayView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_initial(self):
        subproject = SubProject.objects.get(id=self.kwargs['pk'])
        return {
            'subproject': subproject,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subproject = SubProject.objects.get(id=self.kwargs['pk'])
        context['subproject'] = subproject
        context['working_hours'] = subproject.terms.working_hours
        return context

    def get_success_url(self):
        return reverse_lazy('shooting-days-view', kwargs={'pk': self.object.subproject.pk})


def check_toc(request):
    new_datetime = iso8601.parse_date(request.GET.get('start_hour', None))
    subproject = SubProject.objects.get(id=request.GET.get('subproject'))
    previous_date = new_datetime.date() - timedelta(days=1)
    try:
        previous_shooting_day = ShootingDay.objects.get(date=previous_date, subproject=subproject)
    except ObjectDoesNotExist:
        response = {'is_broken': False}
        return JsonResponse(response)
    diff = new_datetime - previous_shooting_day.end_hour
    response = {'is_broken': True} if diff < timedelta(hours=11) else {'is_broken': False}
    return JsonResponse(response)


class DeleteShootingDayView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ShootingDay
    template_name = 'work_logger/delete_form.html'

    def get_success_url(self):
        return reverse_lazy('shooting-days-view', kwargs={'pk': self.object.subproject.pk})

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.subproject.parent.user
        return logged_in_user == content_user


class UpdateShootingDayView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ShootingDay
    template_name = 'work_logger/update_form.html'
    form_class = ShootingDayCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = "SHOOTING DAY"
        return context

    def get_success_url(self):
        return reverse_lazy('subprojects-view', kwargs={'pk': self.object.subproject.pk})

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UpdateShootingDayView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.subproject.parent.user
        return logged_in_user == content_user

class ShootingDayDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ShootingDay
    template_name = 'work_logger/shootingday_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = "SHOOTING DAY"
        return context

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.subproject.parent.user
        return logged_in_user == content_user


class TermsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'work_logger/create_terms.html'
    form_class = TermsCreateForm
    success_message = 'Success: Terms were created.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('subprojects-view', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        user = self.request.user
        f = form.save(commit=False)
        f.user = user
        return super().form_valid(form)


class TermsCreateViewBS(LoginRequiredMixin, BSModalCreateView):
    template_name = 'work_logger/create_terms_bs.html'
    form_class = TermsCreateFormBS
    success_message = 'Success: Terms were created.'
    success_url = reverse_lazy('main-page')

    def form_valid(self, form):
        if not self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form.instance.user = self.request.user
            url = self.request.POST.get('URL')
            super().form_valid(form)
            return HttpResponseRedirect(url)
        else:
            return super().form_invalid(form)


class TermsView(LoginRequiredMixin, FilterView):
    def get_queryset(self):
        return Terms.objects.filter(user=self.request.user)

    model = Terms
    context_object_name = 'object_list'
    filterset_class = TermsFilter
    template_name = 'work_logger/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['pk'])
        return context


class DeleteTermsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Terms
    template_name = 'work_logger/delete_form.html'

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.user
        return logged_in_user == content_user

    def get_success_url(self):
        return reverse_lazy('terms-view',
                            kwargs={'pk': Project.objects.filter(user=self.request.user).first().pk})


class UpdateTermsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Terms
    success_url = reverse_lazy('main-page')
    template_name = 'work_logger/update_form.html'
    form_class = TermsCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = "TERMS"
        return context

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.user
        return logged_in_user == content_user

    def get_success_url(self):
        return reverse_lazy('terms-view',
                            kwargs={'pk': Project.objects.filter(user=self.request.user).first().pk})


class CrewMembersView(LoginRequiredMixin, FilterView):
    def get_queryset(self):
        return CrewMember.objects.filter(user=self.request.user)

    model = CrewMember
    context_object_name = 'object_list'
    filterset_class = CrewMembersFilter
    template_name = 'work_logger/crew_members.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['pk'])
        return context


class CrewMemberCreateView(LoginRequiredMixin, CreateView):
    template_name = 'work_logger/create_crew_member.html'
    form_class = CrewMemberCreateForm
    success_message = 'Success: Crew member created.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        user = self.request.user
        f = form.save(commit=False)
        f.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('crew-members-view', kwargs={'pk': self.kwargs['pk']})


class CrewMemberCreateViewBS(LoginRequiredMixin, BSModalCreateView):
    template_name = 'work_logger/create_crew_member_bs.html'
    form_class = CrewMemberCreateFormBS
    success_message = 'Success: Crew member was created.'
    success_url = reverse_lazy('main-page')

    def form_valid(self, form):
        if not self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form.instance.user = self.request.user
            url = self.request.POST.get('URL')
            super().form_valid(form)
            return HttpResponseRedirect(url)
        else:
            return super().form_invalid(form)


class UpdateCrewMemberView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CrewMember
    template_name = 'work_logger/update_form.html'
    form_class = CrewMemberCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = "CREW MEMBER"
        return context

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.user
        return logged_in_user == content_user

    def get_success_url(self):
        return reverse_lazy('crew-members-view',
                            kwargs={'pk': Project.objects.filter(user=self.request.user).first().pk})


class DeleteCrewMemberView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CrewMember
    template_name = 'work_logger/delete_form.html'

    def test_func(self):
        logged_in_user = self.request.user
        obj = self.get_object()
        content_user = obj.user
        return logged_in_user == content_user

    def get_success_url(self):
        return reverse_lazy('crew-members-view',
                            kwargs={'pk': Project.objects.filter(user=self.request.user).first().pk})
