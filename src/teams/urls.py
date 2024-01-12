from django.urls import path
from teams import views

urlpatterns = [
    path("", views.TeamListCreateView.as_view(), name="teams-list"),
    path(
        "<int:id>",
        views.TeamRetrieveDestroyView.as_view(),
        name="team-detail",
    ),
    path(
        "<int:id>/expenses",
        views.TeamExpenseListView.as_view(),
        name="team-expenses-list",
    ),
    path(
        "<int:id>/expenses/<int:expense_id>",
        views.TeamExpenseRetrieveUpdateDestroyView.as_view(),
        name="team-expense-detail",
    ),
    path(
        "<int:id>/expenses/<int:expense_id>/comments",
        views.TeamExpenseCommentListView.as_view(),
        name="team-expense-comments-list",
    ),
    path(
        "<int:id>/expenses/<int:expense_id>/comments/<int:comment_id>",
        views.TeamExpenseCommentRetrieveDestroyView.as_view(),
        name="team-expense-comments-detail",
    ),
    path(
        "<int:id>/messages",
        views.GroupMessageListView.as_view(),
        name="team-messages",
    ),
    path(
        "<int:id>/transactions",
        views.GroupTransactionListCreateView.as_view(),
        name="team-messages",
    ),
    path("<int:id>/members", views.TeamMembersRetrieveView.as_view()),
    path(
        "<int:id>/invitations",
        views.TeamInviteListCreateView.as_view(),
        name="team-invite",
    ),
    path("join", views.team_join_view, name="team-join"),
    path(
        "<int:id>/debt_reminders",
        views.TeamDebtReminderListCreateView.as_view(),
        name="team-debt-reminder",
    ),
    path(
        "<int:id>/friends_to_invite",
        views.get_friends_to_invite,
        name="team-friends-to-invite",
    ),
    path(
        "<int:id>/info",
        views.get_team_info,
        name="team-info",
    ),
]
