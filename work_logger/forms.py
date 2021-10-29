from bootstrap_modal_forms.mixins import CreateUpdateAjaxMixin
from braces.forms import UserKwargModelFormMixin
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from accounts.models import CustomUser
from django import forms
from django.forms import TextInput, widgets, modelformset_factory
from bootstrap_modal_forms.forms import BSModalModelForm
from work_logger.models import Project, SubProject, Terms, CrewMember, PAY_PERIODS, ShootingDay, WORKING_HOURS


class ProjectCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Project name...'}))
    description = forms.CharField(required=False, max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 4, 'cols': 10}))

    class Meta:
        model = Project
        exclude = ['user']


class SubProjectCreateForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label="Select Project",
                                    widget=forms.Select(attrs={'style': 'width:255px'}))
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '10', 'class': 'form-control', 'placeholder': 'Sub-project name...'}))
    position = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '10', 'class': 'form-control', 'placeholder': 'Position...'}))
    terms = forms.ModelChoiceField(queryset=Terms.objects.all(), empty_label="Select Terms",
                                   widget=forms.Select(attrs={'style': 'width:255px'}))
    crew_members = forms.ModelMultipleChoiceField(required=False, label="Crew Members", queryset=CrewMember.objects.all(),
                                                  widget=forms.SelectMultiple(attrs={'style': 'width:255px'}))
    description = forms.CharField(required=False, max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...', 'rows': 2, 'cols': 10}))

    class Meta:
        model = SubProject
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(SubProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Project.objects.filter(user=user)
        self.fields['terms'].queryset = Terms.objects.filter(user=user)
        self.fields['crew_members'].queryset = CrewMember.objects.filter(user=user)


class ProjectCreateFormBS(UserKwargModelFormMixin, BSModalModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Project name...'}))
    description = forms.CharField(required=False, max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...', 'rows': 4, 'cols': 10}))

    class Meta:
        model = Project
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ProjectCreateFormBS, self).__init__(*args, **kwargs)


class TermsCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Terms name...'}))
    description = forms.CharField(required=False, max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...', 'rows': 2, 'cols': 10}))
    pay_period = forms.ChoiceField(choices=PAY_PERIODS, widget=forms.Select())
    working_hours = forms.ChoiceField(choices=WORKING_HOURS, widget=forms.Select())
    base_rate = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                   'placeholder': 'Base rate...'}))
    ot_rate = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                   'placeholder': 'Overtime rate...'}))
    camera_ot_rate = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                   'placeholder': 'Camera overtime rate...'}))
    extras = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                        'placeholder': 'Extra charges...'}))

    class Meta:
        model = Terms
        exclude = ['user']


class TermsCreateFormBS(BSModalModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Terms name...'}))
    description = forms.CharField(required=False, max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...', 'rows': 2, 'cols': 10}))
    pay_period = forms.ChoiceField(choices=PAY_PERIODS, widget=forms.Select())
    working_hours = forms.ChoiceField(choices=WORKING_HOURS, widget=forms.Select())
    base_rate = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                   'placeholder': 'Base rate...'}))
    ot_rate = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                   'placeholder': 'Overtime rate...'}))
    camera_ot_rate = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                   'placeholder': 'Camera overtime rate...'}))
    extras = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                        'placeholder': 'Extra charges...'}))

    class Meta:
        model = Terms
        exclude = ['user']


class CrewMemberCreateFormBS(BSModalModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Name...'}))
    surname = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Surname...'}))
    position = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Position...'}))
    contact_info = forms.CharField(required=False, max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Contact info...', 'rows': 3, 'cols': 10}))

    class Meta:
        model = CrewMember
        exclude = ['user']


class ShootingDayCreateForm(forms.ModelForm):
    subproject = forms.ModelChoiceField(queryset=SubProject.objects.all(), empty_label="Select sub-project",
                                    widget=forms.Select(attrs={'style': 'width:300px'}))
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '10', 'class': 'form-control', 'placeholder': 'Shooting day name...(i.e. SD01)'}))
    date = forms.DateTimeField(label="Date:", widget=forms.DateInput(attrs={'type': 'date',
                                                                                        'style': 'width:300px'}))
    description = forms.CharField(required=False, max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...', 'rows': 2, 'cols': 10}))
    start_hour = forms.DateTimeField(label="Start hour:", widget=forms.DateTimeInput(attrs={'id': "start_hour", 'type': 'datetime-local',
                                                                                        'style': 'width:300px'}))
    end_hour = forms.DateTimeField(label="End hour:", widget=forms.TimeInput(attrs={'id': "end_hour", 'type': 'datetime-local',
                                                                                        'style': 'width:300px'}))
    extras = forms.DecimalField(widget=forms.NumberInput(attrs={'size': '35', 'class': 'form-control',
                                                                 'placeholder': 'Extra charges...'}))
    ot = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'O/T...', }))
    camera_ot = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Camera O/T...', 'style': 'width:10px'}))
    toc = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                            'placeholder': 'TOC...', 'style': 'width:10px'}))

    class Meta:
        model = ShootingDay
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(ShootingDayCreateForm, self).__init__(*args, **kwargs)
        self.fields['subproject'].queryset = SubProject.objects.filter(parent__user=user)


class CrewMemberCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Name...'}))
    surname = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Surname...'}))
    position = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Position...'}))
    contact_info = forms.CharField(required=False, max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Contact info...', 'rows': 3, 'cols': 10}))

    class Meta:
        model = CrewMember
        exclude = ['user']
