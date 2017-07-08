from django.contrib import admin

# Register your models here.
from itis_manage.models import Test

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass
