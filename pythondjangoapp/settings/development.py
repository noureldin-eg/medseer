from pythondjangoapp.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += (
    # other apps for local development
    'livereload',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.abspath(BASE_DIR), 'db.sqlite3'),
    }
}
