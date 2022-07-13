from django.contrib import admin

# Register your models here.
from main.models import Result, CalculationCount

admin.site.register(Result)
admin.site.register(CalculationCount)