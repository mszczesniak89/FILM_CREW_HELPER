from datetime import datetime

import django_filters
from django_filters import ModelChoiceFilter, ChoiceFilter, CharFilter, NumericRangeFilter, RangeFilter, widgets, DateFilter
from django import forms
from django_filters.widgets import RangeWidget

from work_logger.models import Project, SubProject, ShootingDay


class ProjectFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label="Project name:",
                      widget=forms.TextInput(attrs={'size': 30,'placeholder': 'insert project name'}))
    description = CharFilter(field_name='description', lookup_expr='icontains', label="Description:",
                             widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'insert project description'}))

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['user', ]


class SubProjectFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label="Sub-project name:",
                      widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'insert subproject name'}))
    position = CharFilter(field_name='position', lookup_expr='icontains', label="Position:",
                          widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'insert position'}))
    description = CharFilter(field_name='description', lookup_expr='icontains', label="Description:",
                             widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'insert description'}))

    class Meta:
        model = SubProject
        fields = '__all__'
        exclude = ['parent', 'terms', 'crew_members']


class ShootingDayFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label="Name:",
                      widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'insert name'}))
    date = DateFilter(
        widget=forms.SelectDateWidget(empty_label=["Year", "Month", "Day"], years=range(2000, 2050),
                                      attrs={
                                          'id': 'datepicker'
                                      }
                                      )
    )
    description = CharFilter(field_name='description', lookup_expr='icontains', label="Description:",
                             widget=forms.TextInput(attrs={'size': 30, 'placeholder': 'insert description'}))


    class Meta:
        model = ShootingDay
        fields = '__all__'
        exclude = ['subproject', 'start_hour', 'end_hour', 'ot', 'camera_ot', 'toc', 'extras']

