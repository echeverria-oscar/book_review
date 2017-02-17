from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^books$', views.books),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addbook$', views.addbook),
    url(r'^add$', views.add),
    url(r'^bookreview/(?P<id>\d+)$', views.bookreview, name='bookreview'),
    url(r'^user_review/(?P<id>\d+)$', views.user_review),
    url(r'^profile/(?P<id>\d+)$', views.profile),
]
