from django.db import models
from django.utils import timezone
from const import CURRENCY_CHOICES, Id
from teams.dataclasses import ExpenseShare
from teams.utils import split_amount
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from users.models import CustomUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import m2m_changed


class Team(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    settled_date = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to="team_avatars/", blank=True, null=True)
    members = models.ManyToManyField(CustomUser, related_name="teams")
    currency = models.CharField(
        _("currency"), max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )

    def __str__(self):
        return self.name


class TeamExpense(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="expenses")
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        _("currency"), max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )
    attachments = models.ImageField(
        upload_to="expense_attachments/", blank=True, null=True
    )
    from_user = models.ForeignKey(
        CustomUser, related_name="expenses_paid", on_delete=models.CASCADE
    )
    to_users = models.ManyToManyField(CustomUser, related_name="expenses_shared")
    users_settled = models.ManyToManyField(
        CustomUser, related_name="expenses_settled", default=[from_user]
    )

    def __str__(self):
        to_users_list = ", ".join(str(user) for user in self.to_users.all())
        return f"{self.description}: {self.from_user} -> {to_users_list} : {self.value} {self.currency}"

    @property
    def expense_shares(self) -> dict[Id, ExpenseShare]:
        shares = split_amount(
            float(self.value), self.to_users.count()
        )  # NOTE: Only splitting equally for now
        return {
            user.id: ExpenseShare(
                share,
                self.currency,
                self.team.id,
                self.from_user == user,
                user in self.users_settled.all(),
            )
            for share, user in zip(shares, self.to_users.all())
        }


class TeamExpenseComment(models.Model):
    team_expense = models.ForeignKey(
        TeamExpense, on_delete=models.CASCADE, related_name="comments"
    )
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"{self.user} - {self.text}"


class TeamInvitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="invitations")
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="invitations"
    )
    to_user_email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team}: {self.from_user} -> {self.to_user_email}"


class TeamDebtReminder(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="reminders")
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reminders_sent"
    )
    to_user_email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team}: {self.from_user} -> {self.to_user_email}"


class GroupMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team_messages"
    )
    text = models.TextField(max_length=20000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.text[:10]}.."


class GroupTransaction(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    to_users = models.ManyToManyField(CustomUser, related_name="transactions_shared")
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="group_transactions"
    )
    text = models.TextField(max_length=20000, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.team}: users {self.from_user.id} -> {[user.id for user in self.to_users.all()]}"


@receiver(m2m_changed, sender=GroupTransaction.to_users.through)
def update_team_debtors(sender, instance, **kwargs):
    user_who_want_to_settle = instance.from_user
    users_receiving_transaction = instance.to_users.all()
    for user in users_receiving_transaction:
        user_who_want_to_settle.settle_with(user.id, instance.team.id)
