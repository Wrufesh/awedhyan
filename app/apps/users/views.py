from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView
from rest_framework.reverse import reverse_lazy
from .models import User
from app.apps.users.forms import InstituteAdminUserForm, InstituteUserForm
from app.utils.mixins import DeleteView, UpdateView, CreateView, LoginRequiredMixin


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')


class UserView(LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('user_list')

    def get_form_class(self):
        if self.request.user.is_superuser:
            return InstituteAdminUserForm
        elif 'Institute Admin' in self.request.user.groups_name:
            return InstituteUserForm

    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.instance.save()
            form.instance.groups.add(Group.objects.get(name='Institute Admin'))
        elif 'Institute Admin' in self.request.user.groups_name:
            form.instance.institute = self.request.user.institute
        return super(UserView, self).form_valid(form)


class UserList(UserView, ListView):
    pass


class UserCreate(UserView, CreateView):
    pass


class UserEdit(UserView, UpdateView):
    pass


class UserDelete(UserView, DeleteView):
    pass