from django.contrib.auth.hashers import make_password
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
        varhash = make_password(form.instance.password, None, 'md5')
        form.instance.set_password(varhash)
        if self.request.user.is_superuser:
            form.instance.save()
            form.instance.groups.add(Group.objects.get(name='Institute Admin'))
        elif 'Institute Admin' in self.request.user.groups_name:
            form.instance.institute = self.request.user.institute
        return super(UserView, self).form_valid(form)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.filter(groups__name__in=['Institute Admin'])
        elif 'Institute Admin' in self.request.user.groups_name:
            return User.objects.filter(groups__name__in=['Student', 'Instructor'])


class UserList(UserView, ListView):
    # def get_queryset:
    pass


class UserCreate(UserView, CreateView):
    pass


class UserEdit(UserView, UpdateView):
    pass


class UserDelete(UserView, DeleteView):
    pass