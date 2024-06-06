from django.contrib import admin
from . models import Estimate,Contact,NewAccount
# Register your models here.

admin.site.register(Estimate)
admin.site.register(Contact)
admin.site.register(NewAccount)