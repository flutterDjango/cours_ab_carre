from .base import *  # noqa F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-wi60d($+g--sxcda&9*pz2taj_dm_7=-*o3jeic&i*_jh%gfs="
)

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# try:
#     from .local import *
# except ImportError:
#     pass
