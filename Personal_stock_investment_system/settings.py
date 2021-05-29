"""
Django settings for Personal_stock_investment_system project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%$i^ni_hl_ek^b(^u&0!4vi%=lx!c*6z6%=nlgegldqkfk$v5q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # django 默认引入apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # django-allauth 需要的apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    # 引入主页
    'homepage',
    # 引入app users
    'users',
    # 引入 stock
    'stock',
    # 引入bootstarp
    'bootstrap4',
    # 引入crispy
    # 'crispy_forms'
    # 引入通知
    'notifications',
    # 引入定时任务
    'django_apscheduler',
    # 引入通知
    'my_notification',
    #引入报告
    'report',
]
# 当出现 "SocialApp matching query does not exist" 这种报错的时候就需要更换这个ID
SITE_ID = 1

# allauth 设置 BACKENDS
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
# django-allauth 常见设置
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 强制注册邮箱验证(注册成功后，会发送一封验证邮件，用户必须验证邮箱后，才能登陆)
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  # 登录方式(选择用户名或者邮箱都能登录)
ACCOUNT_EMAIL_REQUIRED = True  # 设置用户注册的时候必须填写邮箱地址
ACCOUNT_LOGOUT_ON_GET = False  # 用户登出(需要确认)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3  # 邮箱确认邮件的截止日期(天数)
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5  # 登录尝试失败的次数
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False  # 更改为True，用户一旦确认他们的电子邮件地址，就会自动登录
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True  # 更改或设置密码后是否自动退出
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False  # 更改为True，用户将在重置密码后自动登录
ACCOUNT_SESSION_REMEMBER = None  # 控制会话的生命周期，可选项还有: "False" 和 "True"
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False  # 用户注册时是否需要输入邮箱两遍
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True  # 用户注册时是否需要用户输入两遍密码
ACCOUNT_USERNAME_BLACKLIST = []  # 用户不能使用的用户名列表
ACCOUNT_UNIQUE_EMAIL = True  # 加强电子邮件地址的唯一性
ACCOUNT_USERNAME_MIN_LENGTH = 6  # 用户名允许的最小长度的整数
SOCIALACCOUNT_AUTO_SIGNUP = True  # 使用从社交账号提供者检索的字段(如用户名、邮件)来绕过注册表单
LOGIN_REDIRECT_URL = "/accounts/profile/"  # 设置登录后跳转链接
ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # 设置退出登录后跳转链接
AUTH_USER_MODEL = 'users.UserProfile'

# 配置邮箱
EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "1649912354@qq.com"
EMAIL_HOST_PASSWORD = "mpqztfnjkrdvhaae"  # 这个不是邮箱密码，而是授权码
EMAIL_USE_TLS = True  # 这里必须是 True，否则发送不成功
EMAIL_FROM = "1649912354@qq.com"  # 发件人
DEFAULT_FROM_EMAIL = "1649912354@qq.com"  # 默认发件人(如果不添加DEFAULT_FROM_EMAIL字段可能会导致如下错误: 451, b'Sender address format error.', 'webmaster@localhost')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Personal_stock_investment_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Personal_stock_investment_system.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')
]
