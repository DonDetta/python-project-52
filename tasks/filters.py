import django_filters
from django import forms
from django.contrib.auth.models import User

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class SelfTasksFilter(django_filters.Filter):
    field_class = forms.BooleanField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', forms.CheckboxInput)
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value and self.parent.request:
            return qs.filter(author=self.parent.request.user)
        return qs


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        empty_label='--------',
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        empty_label='--------',
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        empty_label='--------',
    )
    self_tasks = SelfTasksFilter(label='Только свои задачи')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
