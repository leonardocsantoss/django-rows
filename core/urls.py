# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', ConvertView.as_view(), name='convert'),
]