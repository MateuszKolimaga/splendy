from rest_framework import serializers
from .models import PersonalOperation, PersonalExpense, PersonalIncome


class PersonalOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalOperation
        fields = "__all__"


class PersonalExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalExpense
        fields = "__all__"


class PersonalIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalIncome
        fields = "__all__"
