from .base import *

ALLOWED_HOSTS = ['44.218.38.26', 'helplaw911.com']
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = []

DATABASE = {
	'default':{
		'ENGINE' :'django.db.backends.postgresql_psycopg2',
		'NAME':'helplaw911',
		'USER':'dbmasteruser',
		'PASSWORD':'a103250101!',
		'HOST':'ls-a9fe012c24a71566d94060cf605d7c1856df2fa1.cphqnh8thqig.ap-northeast-2.rds.amazonaws.com'
		'PORT''5432',
		}
	}

