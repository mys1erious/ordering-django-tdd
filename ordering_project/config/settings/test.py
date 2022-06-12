import django.core.mail.backends.locmem

from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ":memory:",
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'