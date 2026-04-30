from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from users.forms import CustomUserCreationForm, CustomUserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)


class UserPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Вы не авторизованы! Пожалуйста, выполните вход.'
            )
            return redirect('login')
        if request.user.pk != int(kwargs['pk']):
            messages.error(
                request, 'У вас нет прав для изменения другого пользователя.'
            )
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UserPermissionMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response


class UserDeleteView(UserPermissionMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, 'Пользователь успешно удален')
        except ProtectedError:
            messages.error(
                self.request,
                'Невозможно удалить пользователя, потому что он используется'
            )
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы залогинены')
        return response

    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Вы разлогинены')
        return redirect('home')
