from datetime import timedelta, datetime
from django.shortcuts import render
from rest_framework import generics
from personal.models import PersonalExpense, PersonalIncome
from personal.serializers import PersonalExpenseSerializer, PersonalIncomeSerializer


class PersonalExpensesListCreateView(generics.ListCreateAPIView):
    queryset = PersonalExpense.objects.all()
    serializer_class = PersonalExpenseSerializer
    days: int | None = None

    def get_queryset(self):
        days = self.request.query_params.get("days")
        if days:
            now = datetime.now()
            start_date = now - timedelta(days=float(days))
            return self.queryset.filter(
                user=self.request.user, date__gte=start_date, date__lte=now
            ).order_by("-date")
        return self.queryset.filter(user=self.request.user).order_by("-date")


class PersonalExpensesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalExpense.objects.all()
    serializer_class = PersonalExpenseSerializer

    def get_queryset(self):
        days = self.request.query_params.get("days")
        if days:
            now = datetime.now()
            start_date = now - timedelta(days=float(days))
            return self.queryset.filter(
                user=self.request.user, date__gte=start_date, date__lte=now
            )
        return self.queryset.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs["id"])


class PersonalIncomesListCreateView(generics.ListCreateAPIView):
    queryset = PersonalIncome.objects.all()
    serializer_class = PersonalIncomeSerializer

    def get_queryset(self):
        days = self.request.query_params.get("days")
        if days:
            now = datetime.now()
            start_date = now - timedelta(days=float(days))
            return self.queryset.filter(
                user=self.request.user, date__gte=start_date, date__lte=now
            ).order_by("-date")
        return self.queryset.filter(user=self.request.user).order_by("-date")


class PersonalIncomesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalIncome.objects.all()
    serializer_class = PersonalIncomeSerializer

    def get_queryset(self):
        days = self.request.query_params.get("days")
        if days:
            now = datetime.now()
            start_date = now - timedelta(days=float(days))
            return self.queryset.filter(
                user=self.request.user, date__gte=start_date, date__lte=now
            )
        return self.queryset.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs["id"])
