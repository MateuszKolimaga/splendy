import json
from rest_framework import serializers
from dataclasses import asdict
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from users.models import CustomUser
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account import app_settings as allauth_account_settings
from allauth.socialaccount.models import EmailAddress
from django.contrib.auth import get_user_model


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "currency", "avatar"]


class TeamMemberSerializer(serializers.ModelSerializer):
    require_context = True
    you_owe = serializers.SerializerMethodField("get_you_owe")
    owes_you = serializers.SerializerMethodField("get_owes_you")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "currency",
            "avatar",
            "you_owe",
            "owes_you",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team_debtors = self.context["team_debtors"]

    def get_owes_you(self, obj):
        try:
            owes_you = self.team_debtors.owes_you.get(obj.id)
            return asdict(owes_you)
        except TypeError:
            return None

    def get_you_owe(self, obj):
        try:
            you_owe = self.team_debtors.you_owe.get(obj.id)
            return asdict(you_owe)
        except TypeError:
            return None


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict["first_name"] = self.validated_data.get("first_name", None)
        data_dict["last_name"] = self.validated_data.get("last_name", None)
        return data_dict

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        try:
            user.save()
        except:
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."),
            )
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


UserModel = get_user_model()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        if hasattr(UserModel, "USERNAME_FIELD"):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, "EMAIL_FIELD"):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, "first_name"):
            extra_fields.append("first_name")
        if hasattr(UserModel, "last_name"):
            extra_fields.append("last_name")
        if hasattr(UserModel, "avatar"):
            extra_fields.append("avatar")
        if hasattr(UserModel, "currency"):
            extra_fields.append("currency")
        model = UserModel
        fields = ("pk", *extra_fields)
        read_only_fields = ("email",)


class CustomUserFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name"]
