from django.db import models
from django.utils.translation import gettext_lazy as _
from const import CURRENCY_CHOICES
from users.models import CustomUser
from django.utils import timezone


class PersonalOperation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    value = models.FloatField(null=False, blank=False)
    currency = models.CharField(
        _("currency"), max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )
    description = models.CharField(max_length=100)
    attachments = models.FileField(upload_to="attachments/", blank=True)

    class Meta:
        abstract = True


class PersonalExpense(PersonalOperation):
    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("transportation", "Transportation"),
        ("utilities", "Utilities"),
        ("entertainment", "Entertainment"),
        ("other", "Other"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.user} {self.date}: {self.value} {self.currency}"


class PersonalIncome(PersonalOperation):
    CATEGORY_CHOICES = [
        ("salary", "Salary"),
        ("bonus", "Bonus"),
        ("investment", "Investment"),
        ("other", "Other"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.user} {self.date}: {self.value} {self.currency}"
