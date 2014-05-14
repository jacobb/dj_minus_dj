from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(
        r'^accounts/login/$',
        view='django.contrib.auth.views.login',
    ),
    url(
        r'^accounts/logout/$',
        view='todo.views.logout_view',
        name="logout"
    ),
    url(
        r'^$',
        view='todo.views.home'
    ),
    url(r'^admin/', include(admin.site.urls)),
)
