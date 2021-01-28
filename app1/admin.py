from django.contrib import admin
from app1.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(LevelPermisions)
admin.site.register(Level)
admin.site.register(LevelMapping)
admin.site.register(Permissionmapping)
admin.site.register(Usermapping)
