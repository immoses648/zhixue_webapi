from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-427d-n0b(!#fft6ucauq@!qqy37^ofk)-vd779w_yysh!(2bb_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ROOT_URLCONF = 'zhixue_webapi.urls'

WSGI_APPLICATION = 'zhixue_webapi.wsgi.application'

TIME_ZONE = 'Asia/Shanghai'
