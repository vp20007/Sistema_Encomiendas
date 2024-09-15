from django.contrib import admin
from .models import CustomUser
from .models import Cliente

admin.site.register(CustomUser)
admin.site.register(Cliente)