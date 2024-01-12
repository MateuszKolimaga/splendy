import copy
from dataclasses import dataclass, field
from dataclasses import astuple

from const import Id


@dataclass
class ExpenseShare:
    value: float
    currency: str
    team: int
    paid: bool = False
    settled: bool = False


@dataclass
class Debt:
    value: float
    currency: str


@dataclass
class Debtors:
    # you = user that makes request for other user debt information
    owes_you: dict[Id, Debt] = field(default_factory=dict)
    you_owe: dict[Id, Debt] = field(default_factory=dict)

    def add_loan(self, user_id: int, expense_share: ExpenseShare, your_currency: str):
        if expense_share.currency != your_currency:
            raise NotImplementedError("Currency conversion not implemented")

        if user_id in self.owes_you:
            self.owes_you[user_id].value += expense_share.value
        else:
            self.owes_you[user_id] = Debt(expense_share.value, expense_share.currency)

    def add_debt(self, user_id: int, expense_share: ExpenseShare, your_currency: str):
        if expense_share.currency != your_currency:
            raise NotImplementedError("Currency conversion not implemented")

        if user_id in self.you_owe:
            self.you_owe[user_id].value += expense_share.value
        else:
            self.you_owe[user_id] = Debt(expense_share.value, expense_share.currency)

    def normalize_debts(self):
        owes_you_deep_copy = copy.deepcopy(self.owes_you)
        for user_id, debt in owes_you_deep_copy.items():
            if user_id in self.you_owe:
                if debt.value > self.you_owe[user_id].value:
                    difference = debt.value - self.you_owe[user_id].value
                    self.you_owe.pop(user_id)
                    self.owes_you[user_id].value = difference
                elif debt.value < self.you_owe[user_id].value:
                    difference = self.you_owe[user_id].value - debt.value
                    self.you_owe[user_id].value = difference
                    self.owes_you.pop(user_id)
                else:
                    self.you_owe.pop(user_id)
                    self.owes_you.pop(user_id)


@dataclass
class TeamDebtors:
    debtors: dict[int, Debtors] = field(default_factory=dict)
