#!/usr/bin/env python
'''
Run this with `$ python ./mini_django.py runserver` and go
to http://localhost:8000/
'''
import os
import sys
from django.conf import settings

# SETTINGS
DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_URLCONF = os.path.splitext(os.path.split(__file__)[1])[0]
DATABASES = {'default': {}}  # required regardless of actual usage
TEMPLATE_DIRS = (
    BASE_DIR,  # Templates in current dir
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.debug',
            ),
        },
    },
]
MIDDLEWARE_CLASSES = ()
SECRET_KEY = 'so so secret'

SILENCED_SYSTEM_CHECKS = ['1_8.W001']  # Silance warning for using TEMPLATE_*

if not settings.configured:
    settings.configure(**locals())


# VIEW
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def service(request, name=None, template='response.xml'):
    context = {
        'host': request.get_host(),
        'service': name or 'fakeService',
    }
    if 'wsdl' in request.GET:
        template = 'wsdl.xml'
    elif name == 'errorService':
        template = 'error_response.xml'
    return render(request, template, context, content_type='text/xml;charset=utf-8')


# URLS
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<name>\w+)?$', service),
]

if __name__ == '__main__':
    # set the ENV
    sys.path += (BASE_DIR,)
    # run the development server
    from django.core import management
    management.execute_from_command_line()
