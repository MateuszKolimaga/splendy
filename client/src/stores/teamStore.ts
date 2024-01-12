import api from '@/common/api'
import { defineStore } from 'pinia'
import GroupOperation from '@/pages/split/models/groupOperations'
import { useToasts } from '@/composables/useToasts'
import { Member } from '@/pages/split/types/member'
import { useUserStore } from './userStore'

const { addToast } = useToasts()
export const useTeamStore = defineStore('team', {
    state: () => ({
        members: <Member[]>[],
        expenses: [],
        comments: [],
        messages: [],
        transactions: [],
        currency: '🪙',
        currentTeam: <null | number>(null),
    }),
    persist: {
        storage: sessionStorage,
    },
    actions: {
        setCurrentTeam(team: number) {
            this.currentTeam = team
        },
        async fetchMembers(teamId: number) {
            this.members = []
            const response = await api.fetch(`teams/${teamId}/members`)
            if ([200, 201, 204].includes(+response.status)) {
                const dbMembers = response.data.members
                //@ts-ignore
                dbMembers.forEach((member) => {
                    this.members.push(
                        new Member(
                            member.id,
                            member.email,
                            member.first_name,
                            member.last_name,
                            member.currency,
                            member.avatar,
                            member.you_owe,
                            member.owes_you
                        )
                    )
                })
                return { success: true }
            }
            return { success: false }
        },
        async fetchExpenses(teamId: number) {
            const response = await api.fetch(`teams/${teamId}/expenses`)
            this.expenses = response.data.results
            return { success: true }
        },
        async fetchComments(teamId: number, expenseId: number) {
            const response = await api.fetch(
                `teams/${teamId}/expenses/${expenseId}/comments`
            )
            this.comments = response.data.results
            return { success: true }
        },
        async fetchMessages(teamId: string) {
            const response = await api.fetch(`teams/${teamId}/messages`)
            //@ts-ignore
            this.messages = response.data.results.sort((a, b) => {
                const timestampA = new Date(a.timestamp).getTime()
                const timestampB = new Date(b.timestamp).getTime()
                return timestampA - timestampB
            })
            return { success: true }
        },
        async fetchTeamInfo(teamId: number) {
            const response = await api.fetch(`teams/${teamId}/info`)
            this.currency = response.data.currency
            return { success: true }
        },
        async unsetTeam() {
            this.members = []
            this.expenses = []
            this.comments = []
            this.messages = []
            this.transactions = []
            this.currency = '🪙'
        },
        async addExpense(expense: GroupOperation) {
            const response = await api.fetch(`teams/${expense.team}/expenses`, {
                method: 'POST',
                body: JSON.stringify(expense),
            })
            if ([200, 201, 204].includes(+response.status)) {
                this.fetchExpenses(expense.team)
                addToast({ message: 'Expense added', type: 'success' })
                return { success: true }
            }
            addToast({ message: 'Failed to add an expense', type: 'danger' })
            return { success: false }
        },
        async deleteExpense(expense: GroupOperation) {
            const response = await api.fetch(
                `teams/${expense.team}/expenses/${expense.id}`,
                { method: 'DELETE' }
            )
            if ([200, 201, 204].includes(+response.status)) {
                //@ts-ignore
                this.expenses = this.expenses.filter((e) => e.id !== expense.id)
                this.fetchExpenses(expense.team)
                addToast({ message: 'Expense deleted', type: 'success' })
                return { success: true }
            }
            this.fetchExpenses(expense.team)
            return { success: true }
        },

        async sendTeamInvitation(email: string, teamId?: number) {
            const response = await api.fetch(`teams/${teamId ?? this.currentTeam}/invitations`, {
                method: 'POST',
                body: JSON.stringify({
                    to_user_email: email,
                    team: teamId ?? this.currentTeam,
                    from_user: useUserStore().user!.id,
                }),
            })
            if ([200, 201, 204].includes(+response.status)) {
                addToast({message: 'Invitation sent', type: 'success'})
                return { success: true }
            }
            addToast({message: 'Failed to send invitation', type: 'danger'})
            return { success: false }
        },
        async sendDebtReminder(email: string, teamId?: number) {
            const response = await api.fetch(`teams/${teamId ?? this.currentTeam}/debt_reminders`, {
                method: 'POST',
                body: JSON.stringify({
                    to_user_email: email,
                    team: teamId ?? this.currentTeam,
                    from_user: useUserStore().user!.id,
                }),
            })
            if ([200, 201, 204].includes(+response.status)) {
                addToast({message: 'Reminder sent', type: 'success'})
                return { success: true }
            } else {
                addToast({ message: 'Failed to send reminder. You can send only 1 reminder per day to every user.', type: 'danger' })
            }
            return { success: false }
        },
        async settleUpWithUser(targetUsers: Member[], teamId?: number) {
            const response = await api.fetch(`teams/${teamId ?? this.currentTeam}/transactions`, {
                method: 'POST',
                body: JSON.stringify({
                    "text": "",
                    "from_user": useUserStore().user!.id,
                    "team": teamId ?? this.currentTeam,
                    "to_users": targetUsers.map((user) => user.id),
                }),
            })
            if ([200, 201, 204].includes(+response.status)) {
                addToast({message: 'Settled up', type: 'success'})
                return { success: true }
            }
            addToast({message: 'Failed to settle up', type: 'danger'})
            return { success: false }
        },
        async fetchFriends(teamId?: number) {
            const response = await api.fetch(`teams/${teamId ?? this.currentTeam}/friends_to_invite`)
            return { success: true, message: response.data.friends }
        },
        async handleInvitation(invitationId: string, showToastIfError: boolean = true) {
            const response = await api.fetch(`teams/join`, {
                method: 'PATCH',
                body: JSON.stringify({
                    "invitation_id": invitationId,
                })
            })
            if ([200, 201, 204].includes(+response.status)) {
                addToast({message: 'Invitation accepted', type: 'success'})
                sessionStorage.removeItem('invitation')
                return { success: true, message: response.data.message }
            } else {
                if (showToastIfError) {
                    addToast({message: response.data.message, type: 'danger'})
                }
                sessionStorage.setItem('invitation', invitationId)
                return { success: false, message: response.data.message }
            }
        }
    },
})
