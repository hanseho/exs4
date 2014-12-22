from django.contrib import admin
from newboard.models import *

# Register your models here.
admin.site.register(Board)
admin.site.register(Article)
admin.site.register(Reply)