from django.contrib import admin

# from myapp.forms import Records
from .models import *
# Register your models here.
admin.site.register(Item)
admin.site.register(record)
admin.site.register(company)
admin.site.register(fuel)
admin.site.register(tank)
admin.site.register(customer)