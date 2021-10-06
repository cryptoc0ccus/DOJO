"""
Django SECRET_KEY generator.
"""
from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

CONFIG_STRING = """
DEBUG=True
SECRET_KEY=%s
ALLOWED_HOSTS=127.0.0.1, .localhost

DEFAULT_FROM_EMAIL ='noreply@bjj.berlin'
EMAIL_HOST='hegemone.uberspace.de'
EMAIL_PORT=587
EMAIL_HOST_PASSWORD='123'
EMAIL_HOST_USER='no-reply@bjj.berlin'
EMAIL_USE_TLS= True

GOOGLE_RECAPTCHA_SECRET_KEY = '6Lf-ae8bAAAAAJ3rxqnObMVFCkHQtbZa44-gNhjA'
GOOGLE_RECAPTCHA_SITE_KEY = '6Lf-ae8bAAAAAAjl7J2FcI3perlSYkR6AaspqOv5'


""".strip() % get_random_string(50, chars)

# Writing our configuration file to '.env'
with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)