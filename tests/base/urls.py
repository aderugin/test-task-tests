# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import TestListView, UserTestingView

urlpatterns = [
    url(r'^$', TestListView.as_view(), name='test-list'),
    url(r'^test/(?P<pk>\d+)/$', UserTestingView.as_view(), name='test-detail')
]
