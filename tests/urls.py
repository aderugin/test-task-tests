# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from tests.base.views import AuthenticationView, RegistrationView, LogoutView


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('tests.base.urls', namespace='tests')),
    url(r'^login/$', AuthenticationView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration')
]
