DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
SECRET_KEY = 'secret'
ROOT_URLCONF = 'tests.urls'
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'social_auth',
    'django_nose',
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = (
    'django_social_auth_appsfuel',
    '--verbosity=2',
    '--nologcapture',
    '--with-doctest',
    '--with-coverage',
    '--cover-package=django_social_auth_appsfuel',
    '--cover-erase',
)
AUTHENTICATION_BACKENDS = (
    'django_social_auth_appsfuel.backend.AppsfuelBackend',
    'django_social_auth_appsfuel.backend.AppsfuelSandboxBackend',
)
APPSFUEL_CLIENT_ID = 'client_id'
APPSFUEL_CLIENT_SECRET = 'client_secret)'