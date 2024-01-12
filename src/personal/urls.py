from django.urls import path
from personal import views

urlpatterns = [
    path(
        "expenses", views.PersonalExpensesListCreateView.as_view(), name="expenses-list"
    ),
    path(
        "expenses/<int:id>",
        views.PersonalExpensesRetrieveUpdateDestroyView.as_view(),
        name="expenses-detail",
    ),
    path("incomes", views.PersonalIncomesListCreateView.as_view(), name="incomes-list"),
    path(
        "incomes/<int:id>",
        views.PersonalIncomesRetrieveUpdateDestroyView.as_view(),
        name="incomes-detail",
    ),
]
