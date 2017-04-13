from django import forms

from app.apps.users.models import User
from app.utils.forms import HTML5BootstrapModelForm
from django.utils.translation import ugettext as _
# from wagtail.wagtailusers.forms import UserEditForm, UserCreationForm, UsernameForm

from app.apps.academy.models import Institute


# class CusUserEditForm(UserEditForm):
#     institute = forms.ModelChoiceField(queryset=Institute.objects.all(), required=False, label=_("Institute"))
#
#
#     def clean(self):
#         cleaned_data = super(CusUserEditForm, self).clean()
#         is_superuser = cleaned_data.get('is_superuser')
#         groups = cleaned_data.get('groups')
#         institute = cleaned_data.get('institute')
#
#         if is_superuser:
#             if groups:
#                 self.add_error('is_superuser', _('Administrator cant have other groups assigned'))
#
#         else:
#             if not institute:
#                 self.add_error('institute', _('This field is required'))
#             if len(groups) != 1:
#                 self.add_error('groups', _('User cannot have more than one groups'))
#
#
# class CusUserCreationForm(UserCreationForm):
#     institute = forms.ModelChoiceField(queryset=Institute.objects, required=False, label=_("Institute"))
#
#     def clean(self):
#         cleaned_data = super(CusUserCreationForm, self).clean()
#         is_superuser = cleaned_data.get('is_superuser')
#         groups = cleaned_data.get('groups')
#         institute = cleaned_data.get('institute')
#
#         if is_superuser:
#             if groups:
#                 self.add_error('is_superuser', _('Administrator cant have other groups assigned'))
#
#         else:
#             if not institute:
#                 self.add_error('institute', _('This field is required'))
#             if len(groups) != 1:
#                 self.add_error('groups', _('User cannot have more than one groups'))


class InstituteUserForm(HTML5BootstrapModelForm):
    # pass
    # TODO save admin institute as view with this form can only be used by Institute Admin
    # def save(self):
    class Meta:
        model = User
        fields = ('username', 'password','first_name', 'last_name', 'email', 'groups')


class InstituteAdminUserForm(HTML5BootstrapModelForm):
    # pass
    # TODO save admin institute as view with this form can only be used by Institute Admin
    # def save(self):

    class Meta:
        model = User
        fields = ('username', 'password','first_name', 'last_name', 'email', 'institute')



# class InstituteUserCreationForm(UserCreationForm):
    # institute = forms.ModelChoiceField(queryset=Institute.objects, required=False, label=_("Institute"))

