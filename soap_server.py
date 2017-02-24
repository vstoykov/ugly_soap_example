#!/usr/bin/env python
'''
Run this with `$ python ./soap_server.py` and go
to http://localhost:8000/
'''
import os
import sys
import django
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
MIDDLEWARE_CLASSES = MIDDLEWARE = ()
SECRET_KEY = 'so so secret'

SILENCED_SYSTEM_CHECKS = [
    '1_8.W001',  # Silance warning for using TEMPLATE_*
    '1_10.W001',  # Silance warning for using MIDDLEWARE_CLASSES
]

if not settings.configured:
    settings.configure(**locals())
    if hasattr(django, 'setup'):
        django.setup()


# Imports after Django is configured
from django.conf.urls import url  # NOQA
from django.shortcuts import render  # NOQA
from django.views.decorators.csrf import csrf_exempt  # NOQA


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


urlpatterns = [
    url(r'^(?P<name>\w+)?$', service),
]


if __name__ == '__main__':
    # set the ENV
    sys.path += (BASE_DIR,)
    # run the development server
    from django.core import management
    management.call_command('runserver', *sys.argv[1:])
