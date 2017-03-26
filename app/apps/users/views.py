from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView
from rest_framework.reverse import reverse_lazy
from .models import User
from app.apps.users.forms import UserForm
from app.utils.mixins import DeleteView, UpdateView, CreateView, LoginRequiredMixin


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')


class UserView(LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('user_list')
    form_class = UserForm


class UserList(UserView, ListView):
    pass


class UserCreate(UserView, CreateView):
    pass


class UserEdit(UserView, UpdateView):
    pass


class UserDelete(UserView, DeleteView):
    pass