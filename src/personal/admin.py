from django.contrib import admin

from personal.models import PersonalExpense, PersonalIncome

# Register your models here.
admin.site.register(PersonalIncome)
admin.site.register(PersonalExpense)
