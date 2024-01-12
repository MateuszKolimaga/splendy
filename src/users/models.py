from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from const import CURRENCY_CHOICES, Id
from teams.dataclasses import Debtors, ExpenseShare, TeamDebtors
from .managers import CustomUserManager
from django.core.files import File
from django.db.models import Q


class CustomUser(AbstractUser):
    username = None  # type:ignore
    email = models.EmailField(_("email adress"), unique=True)
    avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)
    currency = models.CharField(
        _("currency"), max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()  # type: ignore

    def __str__(self):
        return self.email

    def team_debtors(self, team_id: int) -> Debtors:
        debtors = Debtors()
        expenses_shared_in_team = [
            expense_shared
            for expense_shared in self.expenses_shared.filter(Q(team_id=team_id))
        ]
        for expense in expenses_shared_in_team:
            settled_users = list(
                expense.users_settled.all().values_list("id", flat=True)
            )
            if expense.from_user.id == self.id:
                for user_id, expense_share in expense.expense_shares.items():
                    if user_id != self.id and user_id not in settled_users:
                        debtors.add_loan(user_id, expense_share, self.currency)
            else:
                debt = expense.expense_shares.get(self.id)
                if debt and self.id not in settled_users:
                    debtors.add_debt(expense.from_user.id, debt, self.currency)
        debtors.normalize_debts()
        return debtors

    def settle_with(self, user_id: int, team_id: int):
        team = self.teams.get(id=team_id)
        user_to_settle = team.members.get(id=user_id)
        team_expenses = team.expenses.all()
        for team_expense in team_expenses:
            if team_expense.from_user.id in [user_to_settle.id, self.id]:
                team_expense.users_settled.add(self)
                team_expense.users_settled.add(user_to_settle)
                team_expense.save()

    def get_friends(self, team_id_to_exclude: int | None = None):
        friends = set()
        excluded_team = (
            self.teams.get(id=team_id_to_exclude) if team_id_to_exclude else None
        )
        for team in self.teams.filter(~Q(id=team_id_to_exclude)):
            for member in team.members.all():
                if member.id != self.id and member not in excluded_team.members.all():
                    friends.add(member)
        return friends
