from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from accounts.models import CustomUser
from django import forms
from django.forms import TextInput, widgets, modelformset_factory
from bootstrap_modal_forms.forms import BSModalModelForm
from work_logger.models import Project, SubProject, Terms, CrewMember, PAY_PERIODS


class ProjectCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Project name...'}))
    description = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description'}))

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
    description = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...', 'rows': 4, 'cols': 10}))

    class Meta:
        model = SubProject
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(SubProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Project.objects.filter(user=user)
        self.fields['terms'].queryset = Terms.objects.filter(user=user)
        self.fields['crew_members'].queryset = CrewMember.objects.filter(user=user)


class ProjectCreateFormBS(BSModalModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Project name...'}))
    description = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...'}))

    class Meta:
        model = Project
        exclude = ['user']


class TermsCreateFormBS(BSModalModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'size': '35', 'class': 'form-control', 'placeholder': 'Terms name...'}))
    description = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...'}))
    pay_period = forms.ChoiceField(choices=PAY_PERIODS, widget=forms.Select(attrs={'style': 'width:420px'}))
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
    contact_info = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Contact info...'}))

    class Meta:
        model = CrewMember
        exclude = ['user']




