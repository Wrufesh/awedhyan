"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import, unicode_literals

# import patterns as patterns
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

# from app.apps.academy.api import ChapterQuestionViewSet
from app.apps.academy import urls as academy_urls
from app.apps.academy.api import CourseChapterPageViewset
from app.apps.users import urls as users_urls

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'chapterquestion', ChapterQuestionViewSet, base_name='chapterquestion')
router.register(r'coursechapters', CourseChapterPageViewset, base_name='coursechapters')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # TODO below namespace='aadhyan' to namespace='academy' and all 'aadhan' namespace used
    url(r'^academy/', include(academy_urls, namespace='aadhyan')),
    url(r'^users/', include(users_urls)),
    url(r'^api/', include(router.urls)),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
