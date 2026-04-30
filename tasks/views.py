from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from tasks.filters import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно создана')
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно изменена')
        return response


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.object = self.get_object()
            if self.object.author != request.user:
                messages.error(
                    request, 'Задачу может удалить только ее автор'
                )
                return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно удалена')
        return super().form_valid(form)
