from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Listing)
admin.site.register(models.User)
admin.site.register(models.Comment)
admin.site.register(models.Bid)
admin.site.register(models.Category)

