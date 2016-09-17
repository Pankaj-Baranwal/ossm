from django.contrib.auth.decorators import login_required
from django.contrib import admin


admin.autodiscover()
admin.site.site_title = 'Convoke 1.0'
admin.site.site_header = 'Convoke 1.0'
admin.site.login = login_required(admin.site.login)

urls = admin.site.urls
