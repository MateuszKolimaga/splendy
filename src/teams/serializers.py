from rest_framework.serializers import ModelSerializer, SerializerMethodField

from teams.models import (
    GroupMessage,
    GroupTransaction,
    Team,
    TeamDebtReminder,
    TeamExpense,
    TeamExpenseComment,
    TeamInvitation,
)
from users.serializers import CustomUserSerializer, TeamMemberSerializer
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "created_date",
            "settled_date",
            "avatar",
            "members",
            "currency",
        ]


class TeamMembersSerializer(serializers.ModelSerializer):
    members = SerializerMethodField("get_members_serializer")

    class Meta:
        model = Team
        fields = ["members"]

    @extend_schema_field(CustomUserSerializer(many=True))
    def get_members_serializer(self, obj):
        team_debtors = self.context["request"].user.team_debtors(obj.id)
        return TeamMemberSerializer(
            obj.members, many=True, context={"team_debtors": team_debtors}
        ).data


class TeamExpenseSerializer(ModelSerializer):
    class Meta:
        model = TeamExpense
        fields = [
            "id",
            "date",
            "value",
            "currency",
            "description",
            "attachments",
            "from_user",
            "to_users",
            "users_settled",
            "team",
        ]


class TeamExpenseCommentSerializer(ModelSerializer):
    class Meta:
        model = TeamExpenseComment
        fields = ["id", "date", "text", "user", "team_expense"]


class GroupMessageSerializer(ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = "__all__"


class GroupTransactionSerializer(ModelSerializer):
    class Meta:
        model = GroupTransaction
        fields = "__all__"


class TeamInvitationSerializer(ModelSerializer):
    class Meta:
        model = TeamInvitation
        fields = "__all__"


class TeamDebtReminderSerializer(ModelSerializer):
    class Meta:
        model = TeamDebtReminder
        fields = "__all__"
