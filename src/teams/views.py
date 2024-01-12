import os
from rest_framework import generics
from splendy import settings
from users.models import CustomUser
from django.conf import settings
from users.serializers import CustomUserSerializer
from .models import (
    GroupMessage,
    GroupTransaction,
    Team,
    TeamDebtReminder,
    TeamExpense,
    TeamExpenseComment,
    TeamInvitation,
)
from .serializers import (
    GroupMessageSerializer,
    GroupTransactionSerializer,
    TeamDebtReminderSerializer,
    TeamExpenseCommentSerializer,
    TeamExpenseSerializer,
    TeamInvitationSerializer,
    TeamMembersSerializer,
    TeamSerializer,
)
from rest_framework import mixins
from django.contrib.auth.models import AnonymousUser
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.exceptions import ValidationError


class TeamListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not isinstance(user, AnonymousUser):
            return self.queryset.filter(id__in=user.teams.all()).order_by("id")
        return self.queryset.none()


class TeamMembersRetrieveView(generics.RetrieveAPIView):
    serializer_class = TeamMembersSerializer
    queryset = Team.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        if not isinstance(user, AnonymousUser):
            return self.queryset
        return self.queryset.none()


class TeamRetrieveDestroyView(generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = "id"


class TeamExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamExpense.objects.all()
    serializer_class = TeamExpenseSerializer

    def get_queryset(self):
        return self.queryset.filter(team=self.kwargs["id"])

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs["expense_id"])


class TeamExpenseListView(generics.ListCreateAPIView):
    queryset = TeamExpense.objects.all()
    serializer_class = TeamExpenseSerializer

    def get_queryset(self):
        return self.queryset.filter(team=self.kwargs["id"]).order_by("-date")


class TeamExpenseCommentListView(generics.ListAPIView):
    queryset = TeamExpenseComment.objects.all()
    serializer_class = TeamExpenseCommentSerializer

    def get_queryset(self):
        return TeamExpenseComment.objects.filter(id=self.kwargs.get("team_expense_id"))


class TeamExpenseCommentRetrieveDestroyView(
    generics.RetrieveAPIView, generics.DestroyAPIView
):
    queryset = TeamExpenseComment.objects.all()
    serializer_class = TeamExpenseCommentSerializer

    def get_queryset(self):
        return self.queryset.filter(team_expense=self.kwargs["expense_id"])

    def get_object(self):
        return self.get_queryset().filter(id=self.kwargs.get("comment_id"))


class GroupMessageListView(generics.ListAPIView):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer

    def get_queryset(self):
        return self.queryset.filter(team=self.kwargs["id"]).order_by("-timestamp")


class TeamInviteListCreateView(generics.ListCreateAPIView):
    queryset = TeamInvitation.objects.all()
    serializer_class = TeamInvitationSerializer

    def get_queryset(self):
        return self.queryset.filter(team=self.kwargs["id"])

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = f"You're invited to join the team: {instance.team.name}!"
        invitation_link = f"{settings.FRONTEND_URL}/?invitation={instance.id}"
        content = f"Click the link below to accept the invitation:"
        html_content = f"""
        <html>
            <body>
                <h2>Hello!</h2>
                <p>{content}</p>
                <a href="{invitation_link}">Accept Invitation</a>
            </body>
        </html>
        """

        message = Mail(
            from_email="tester.kolimaga@gmail.com",  # TODO: change to real email
            to_emails=instance.to_user_email,
            subject=subject,
            html_content=html_content,
        )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(str(e))


class GroupTransactionListCreateView(generics.ListCreateAPIView):
    queryset = GroupTransaction.objects.all()
    serializer_class = GroupTransactionSerializer

    def get_queryset(self):
        return self.queryset.filter(team=self.kwargs["id"]).order_by("-date")


class TeamDebtReminderListCreateView(generics.ListCreateAPIView):
    queryset = TeamDebtReminder.objects.all()
    serializer_class = TeamDebtReminderSerializer

    def get_queryset(self):
        return self.queryset.filter(team=self.kwargs["id"])

    def perform_create(self, serializer):
        now = datetime.now()
        existing_reminder = TeamDebtReminder.objects.filter(
            to_user_email=serializer.validated_data["to_user_email"],
            date__range=[now - timedelta(days=1), now],
        ).exists()

        if existing_reminder:
            raise ValidationError(
                "Reminder already exists within the specified date range"
            )

        instance = serializer.save()

        subject = f"Splendy: {instance.from_user.first_name} {instance.from_user.last_name} sent you a payment reminder."
        content = f"User {instance.from_user.first_name} {instance.from_user.last_name} sent you a reminder about the existing arrears in team {instance.team.name}."
        html_content = f"""
        <html>
            <body>
                <h2>Hello!</h2>
                <p>{content}</p>
            </body>
        </html>
        """

        message = Mail(
            from_email="tester.kolimaga@gmail.com",  # TODO: change to real email
            to_emails=instance.to_user_email,
            subject=subject,
            html_content=html_content,
        )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(str(e))


@api_view(["PATCH"])
def team_join_view(request):
    invitation_id = request.data.get("invitation_id")
    user = request.user
    if user.is_anonymous:
        return Response(
            {"message": "Login or create an account in order to accept invitation"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        invitation = TeamInvitation.objects.get(id=invitation_id)

        if invitation.to_user_email != user.email:
            return Response(
                {
                    "message": "Logout and login with the correct user in order to accept invitation"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if invitation.team.members.filter(id=user.id).exists():
            return Response(
                {"message": "User already in the team"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        team = invitation.team
        team.members.add(user)
        team.save()
        invitation.delete()

        return Response(
            {"message": "Invitation accepted and user added to the team"},
            status=status.HTTP_200_OK,
        )
    except (TeamInvitation.DoesNotExist, CustomUser.DoesNotExist) as error:
        print(str(error))
        return Response(
            {"message": "Invalid invitation or user"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def get_friends_to_invite(request, id):
    user = request.user
    if user.is_anonymous:
        return Response(
            {"error": "User is anonymous."}, status=status.HTTP_401_UNAUTHORIZED
        )
    friends = user.get_friends(team_id_to_exclude=id)
    serializer = CustomUserSerializer(friends, many=True)
    return Response({"friends": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_team_info(request, id):
    user = request.user
    if user.is_anonymous:
        return Response(
            {"error": "User is anonymous."}, status=status.HTTP_401_UNAUTHORIZED
        )
    team = Team.objects.get(id=id)
    serializer = TeamSerializer(team)
    return Response(
        {"currency": serializer.data["currency"]}, status=status.HTTP_200_OK
    )
