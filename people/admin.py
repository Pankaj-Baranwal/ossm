from django.contrib import admin

from . import models

admin.site.register(models.Subscription, admin.ModelAdmin)
admin.site.register(models.EmailRead, admin.ModelAdmin)
admin.site.register(models.User, admin.ModelAdmin)
