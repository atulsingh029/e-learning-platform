allowed_hosts = ['*']
debug = True
secret_key = 'secret key here'

# SMTP setup
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'primestudies.glau@gmail.com'
EMAIL_HOST_PASSWORD = 'fJca57ezPseRSpp'
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
