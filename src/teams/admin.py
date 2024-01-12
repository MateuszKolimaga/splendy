from django.contrib import admin

from teams.models import (
    GroupTransaction,
    Team,
    TeamExpense,
    GroupMessage,
    TeamInvitation,
)

# Register your models here.
admin.site.register(Team)
admin.site.register(TeamExpense)
admin.site.register(GroupMessage)
admin.site.register(GroupTransaction)
admin.site.register(TeamInvitation)
