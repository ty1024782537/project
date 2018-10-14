from django.contrib import admin

# Register your models here.
from order.models import Hauling


@admin.register(Hauling)
class HaulingAdmin(admin.ModelAdmin):
    pass
