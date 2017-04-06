# from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from .views import *

urlpatterns = [
    # CRUD BoardOrUniversity
    url(r'^board/list/$', BoardList.as_view(), name='board_list'),
    url(r'^board/create/$', BoardCreate.as_view(), name='board_add'),
    url(r'^board/update/(?P<pk>[0-9]+)/$', BoardEdit.as_view(), name='board_edit'),
    url(r'^board/delete/(?P<pk>[0-9]+)/$', BoardDelete.as_view(), name='board_delete'),
    # CRUD Institute
    url(r'^institute/list/$', InstituteList.as_view(), name='institute_list'),
    url(r'^institute/create/$', InstituteCreate.as_view(), name='institute_add'),
    url(r'^institute/update/(?P<pk>[0-9]+)/$', InstituteEdit.as_view(), name='institute_edit'),
    url(r'^institute/delete/(?P<pk>[0-9]+)/$', InstituteDelete.as_view(), name='institute_delete'),
    # CRUD Faculty
    url(r'^faculty/list/$', FacultyList.as_view(), name='faculty_list'),
    url(r'^faculty/create/$', FacultyCreate.as_view(), name='faculty_add'),
    url(r'^faculty/update/(?P<pk>[0-9]+)/$', FacultyEdit.as_view(), name='faculty_edit'),
    url(r'^faculty/delete/(?P<pk>[0-9]+)/$', FacultyDelete.as_view(), name='faculty_delete'),
    # CRUD Program
    url(r'^program/list/$', ProgramList.as_view(), name='program_list'),
    url(r'^program/create/$', ProgramCreate.as_view(), name='program_add'),
    url(r'^program/update/(?P<pk>[0-9]+)/$', ProgramEdit.as_view(), name='program_edit'),
    url(r'^program/delete/(?P<pk>[0-9]+)/$', ProgramDelete.as_view(), name='program_delete'),
    # CRUD ProgramLevel
    url(r'^programlevel/list/$', ProgramLevelList.as_view(), name='programlevel_list'),
    url(r'^programlevel/create/$', ProgramLevelCreate.as_view(), name='programlevel_add'),
    url(r'^programlevel/update/(?P<pk>[0-9]+)/$', ProgramLevelEdit.as_view(), name='programlevel_edit'),
    url(r'^programlevel/delete/(?P<pk>[0-9]+)/$', ProgramLevelDelete.as_view(), name='programlevel_delete'),
    # CRUD Course
    url(r'^course/list/$', CourseList.as_view(), name='course_list'),
    url(r'^course/create/$', CourseCreate.as_view(), name='course_add'),
    url(r'^course/update/(?P<pk>[0-9]+)/$', CourseEdit.as_view(), name='course_edit'),
    url(r'^course/delete/(?P<pk>[0-9]+)/$', CourseDelete.as_view(), name='course_delete'),
    # CRUD Institute User
    url(r'^institute/user/list/$', InstituteUserList.as_view(), name='instituteuser_list'),
    url(r'^institute/user/create/$', InstituteUserCreate.as_view(), name='instituteuser_add'),
    url(r'^institute/user/update/(?P<pk>[0-9]+)/$', InstituteUserEdit.as_view(), name='instituteuser_edit'),
    url(r'^institute/user/delete/(?P<pk>[0-9]+)/$', InstituteUserDelete.as_view(), name='instituteuser_delete'),
    # CRUD Chapter
    url(r'^chapter/list/(?P<course_id>[0-9]+)/$', ChapterList.as_view(), name='chapter_list'),
    url(r'^chapter/create/(?P<course_id>[0-9]+)/$', ChapterCreate.as_view(), name='chapter_add'),
    url(r'^chapter/update/(?P<course_id>[0-9]+)/(?P<pk>[0-9]+)/$', ChapterEdit.as_view(), name='chapter_edit'),
    url(r'^chapter/delete/(?P<course_id>[0-9]+)/(?P<pk>[0-9]+)/$', ChapterDelete.as_view(), name='chapter_delete'),

    # Chapter Questions
    url(r'^chapterquestions/add/(?P<chapter_id>[0-9]+)/$', ChapterQuestion.as_view(), name='chapterquestions_add'),

    # Create Test
    url(r'^test/list/$', TestListView.as_view(), name='test_add'),
    url(r'^test/create/$', TestCreateEditView.as_view(), name='test_add'),
    url(r'^test/update/(?P<test_id>[0-9]+)/$', TestCreateEditView.as_view(), name='test_edit'),
    url(r'^test/delete/(?P<test_id>[0-9]+)/$', TestDeleteView.as_view(), name='test_delete'),

    # Quiz
    url(r'^chapter/quiz/(?P<chapter_id>[0-9]+)/$$', QuizView.as_view(), name='chapter_quiz'),
    url(r'^test/quiz/(?P<test_id>[0-9]+)/$$', QuizView.as_view(), name='test_quiz'),

]
