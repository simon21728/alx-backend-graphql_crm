INSTALLED_APPS = [
    # ... your other apps ...
    'django_crontab',
]

CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]