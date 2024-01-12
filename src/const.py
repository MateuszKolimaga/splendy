import currencies
from typing import TypeAlias

Id: TypeAlias = int
CURRENCY_CHOICES = [(curr, curr) for curr in currencies.MONEY_FORMATS.keys()]
