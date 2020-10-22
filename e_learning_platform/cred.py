allowed_hosts = ['*']
debug = True
secret_key = 'secret key here'

# SMTP setup
EMAIL_HOST = 'host'
EMAIL_HOST_USER = 'email'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
