<template lang="pug">
.container-fluid.gx-0
      .row.d-flex.gx-0
          .members-panel.fixed-h.col-4.bg-light.p-0.border-end.d-flex.flex-column
              .panel-header.p-4.bg-light.border.border-end-0
                  .d-flex.flex-row.align-items-center.justify-content-between
                      .d-flex.flex-row.align-items-center.gap-2
                        .flex-grow-1.fw-bold.ms-3 
                            | Members
                        .text-muted.spinner-border.spinner-border-sm.ms-1(v-if="showMembersUpdating || showMembersSpinner")
                        //- .text-muted.ms-1(v-if="showMembersUpdating") Updating
                      group-avatar.d-inline-block.mx-2(:group="currentTeam").mx-2.invisible
                      .d-flex.flex-row.align-items-center.gap-2.flex-end.flex-shrink-1
                        .text-muted.mx-2(v-if="members.length > 1" @click="toggleMembersDetails" style="cursor: pointer;") {{ membersDetailsShown ? 'Hide' : 'Show' }} details
                        button.btn.btn-primary(@click="openAddMemberDialog")
                            font-awesome-icon(icon="plus" style={'color': 'white'})
              //- .panel-body.overflow-y-auto.flex-grow-1.pt-2(v-if="showMembersSpinner")
              //-   .d-flex.flex-column.align-items-center.justify-content-center.h-100
              //-           .spinner-border
              .panel-body.overflow-y-auto.flex-grow-1.pt-2(v-if="members.length > 1")
                MemberTile(v-for="member in membersWithoutUser" :key="member.id", :member="member", :showDetails="membersDetailsShown" @settle-up="handleSettleUp")
              .panel-body.overflow-y-auto.flex-grow-1.pt-3(v-else)
                .d-flex.flex-column.align-items-center.justify-content-center.h-100
                    .text-muted(v-if="!showMembersUpdating && !showMembersSpinner") No members yet (except you)
                    .text-muted.mt-2(v-if="!showMembersUpdating && !showMembersSpinner" @click="openAddMemberDialog" style="cursor: pointer;") Invite some friends
                    .text-muted(v-else) Fetching members and debts...
              .panel-footer.flex-grow-2
                .d-flex.flex-row.justify-content-around.w-100.align-content-center.border-top.py-3
                  .d-flex.flex-column.justify-content-center(v-if="sumTheyOwe > 0")
                    .text-success They owe you:
                    .d-flex.flex-row.justify-content-center.align-items-center
                      .fw-bold.me-1 {{ sumTheyOwe.toFixed(2) }} 
                      .text {{ currency  }}
                  .d-flex.flex-column.justify-content-center(v-if="sumYouOwe > 0")
                    .text-warning You owe them:
                    .d-flex.flex-row.justify-content-center.align-items-center
                      .fw-bold.me-1 {{ sumYouOwe.toFixed(2) }} 
                      .text {{ currency  }}
          .center-panel.col-8.fixed-h.bg-light.border-top.d-flex.flex-column
                .group-info.p-4.border-bottom.d-flex.flex-row.align-items-center
                    .group-info-wrapper.w-100.d-flex.flex-row.align-items-center
                      group-avatar.d-inline-block.mx-2(:group="currentTeam")
                      .d-inline-block.ms-3.fw-bold {{ currentTeam.name }}
                      .d-inline-block.ms-3
                          font-awesome-icon(icon="comments" @click="isChatOpen=true" style="cursor: pointer")
                      .d-inline.text-muted.spinner-border.spinner-border-sm.ms-3(v-if="showExpensesUpdating || showExpensesSpinner")
                      //- .d-inline.text-muted.ms-3(v-if="showExpensesUpdating") Updating
                    button.btn.btn-outline-secondary.mx-3(v-if="newExpensesReceived" @click="refreshAll" ).flex-end.flex-shrink-1
                      .d-flex.flex-row.align-items-center
                        .text-white.text-no-wrap.me-2.text-success Refresh
                        font-awesome-icon.text-success(icon="refresh")
                    button.btn.btn-primary(@click="openAddGroupExpenseDialog").flex-end.flex-shrink-1
                      font-awesome-icon(icon="plus" style={'color': 'white'})
                .group-operations-body.px-3.overflow-y-auto.flex-grow-1.pt-3(v-if="showExpensesUpdating || showExpensesSpinner")
                  .d-flex.flex-column.align-items-center.justify-content-center.h-100
                    .text-muted Calculating expenses...
                .group-operations-body.px-3.pt-2.overflow-y-auto(v-else-if="expenses.length > 0")
                  template(v-for="(expense, gIndex) in expenses", :key="expense.id")
                    GroupOperationTile(:groupOperation="expense")
                    .group-operations-footer.px-3(v-if="expenses[gIndex+1]?.date.slice(0,10) !== expense.date.slice(0,10) && gIndex < expenses.length - 1")
                      .d-flex.flex-row.justify-content-center.align-items-center
                        .w-100.border-top
                .group-operations-body.px-3.pt-2.flex-grow-1.pt-3(v-else)
                    .d-flex.flex-column.align-items-center.justify-content-center.h-100
                      .text-muted(v-if="!showExpensesUpdating") No group expenses yet
                      .text-muted.mt-2(v-if="members.length < 2 && !showExpensesUpdating" @click="openAddMemberDialog" style="cursor: pointer;") Invite some friends and then add expenses
ChatComponent(v-if="isChatOpen", :groupId="teamId" @close="isChatOpen=false")
AddMemberDialog(v-if="isAddMemberDialogOpen", :friends="friends" @close="closeAddMemberDialog")
AddGroupExpenseDialog(v-if="isAddGroupExpenseDialogOpen", :groupId="currentTeam.id", :members="members", @close="closeAddGroupExpenseDialog" @execute="handleYourNewExpense")
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import IconTextButton from '@/components/button/IconTextButton.vue'
import ChartComponent from '@/components/chart/pie/ChartComponent.vue'
import GroupTile from '@/components/split-components/GroupTile.vue'
import MemberTile from '@/components/split-components/MemberTile.vue'
import GroupOperationTile from '@/components/split-components/GroupOperationTile.vue'
import AddMemberDialog from '@/components/split-components/modals/AddMemberDialog.vue'
import AddGroupExpenseDialog from '@/components/split-components/modals/AddGroupExpenseDialog.vue'
import AddGroupDialog from '@/components/split-components/modals/AddGroupDialog.vue'
import ChatComponent from '@/components/split-components/ChatComponent.vue'
import { useTeamStore } from '@/stores/teamStore'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/userStore'
import { useSocialStore } from '@/stores/socialStore'
import GroupAvatar from '@/components/group/GroupAvatar.vue'
import { useToasts } from '@/composables/useToasts'
import api from '@/common/api'
import { User } from './types/user'

export default defineComponent({
    name: 'DashboardSplitPage',
    components: {
        ChartComponent,
        GroupTile,
        MemberTile,
        GroupOperationTile,
        IconTextButton,
        AddMemberDialog,
        AddGroupExpenseDialog,
        AddGroupDialog,
        ChatComponent,
        GroupAvatar,
    },
    props: {
        teamId: String,
    },
    setup(props) {
        const teamId = +props.teamId!
        const memberClicked = ref(false)
        const isAddMemberDialogOpen = ref(false)
        const isAddGroupExpenseDialogOpen = ref(false)
        const isChatOpen = ref(false)
        const membersDetailsShown = ref(false)
        const socialStore = useSocialStore()
        const { teams } = storeToRefs(socialStore)
        const teamStore = useTeamStore()
        const userStore = useUserStore()
        const { user } = storeToRefs(userStore)
        const { currency, expenses, members } = storeToRefs(teamStore)
        const showExpensesSpinner = ref(true)
        const showMembersSpinner = ref(true)
        const showMembersUpdating = ref(false)
        const showExpensesUpdating = ref(false)
        const friends = ref(undefined)
        const newExpensesReceived = ref(false)
        const socket = ref<WebSocket | null>(null)
        const currentTeam = teams.value.find(
            //@ts-ignore
            (team) => team.id == teamId
        )
        teamStore.setCurrentTeam(teamId)
        teamStore.fetchTeamInfo(teamId)
        teamStore
            .fetchMembers(teamId)
            .then(() => (showMembersSpinner.value = false))
        teamStore
            .fetchExpenses(teamId)
            .then(() => (showExpensesSpinner.value = false))
        teamStore.fetchFriends(teamId).then((result) => {
            friends.value = result.message
        })

        const { addToast } = useToasts()

        return {
            currentTeam,
            memberClicked,
            friends,
            user,
            members,
            expenses,
            isAddMemberDialogOpen,
            isAddGroupExpenseDialogOpen,
            isChatOpen,
            membersDetailsShown,
            showMembersSpinner,
            showExpensesSpinner,
            addToast,
            teamStore,
            userStore,
            newExpensesReceived,
            socket,
            showMembersUpdating,
            showExpensesUpdating,
            currency,
        }
    },
    mounted() {
        this.subscribeToOtherUsersActions()
    },
    methods: {
        openAddMemberDialog() {
            this.isAddMemberDialogOpen = true
        },
        closeAddMemberDialog() {
            this.isAddMemberDialogOpen = false
        },
        openAddGroupExpenseDialog() {
            if (this.members.length == 1) {
                this.addToast({
                    message:
                        'You have to add at least one member to add an expense',
                    type: 'warning',
                })
                return
            }
            this.isAddGroupExpenseDialogOpen = true
        },
        closeAddGroupExpenseDialog() {
            this.isAddGroupExpenseDialogOpen = false
        },
        handleYourNewExpense() {
            this.refreshMembers()
            this.sendWebsocketMessage()
            this.closeAddGroupExpenseDialog()
        },
        handleSettleUp() {
            this.refreshExpenses()
            this.refreshMembers()
            this.sendWebsocketMessage()
        },
        async refreshMembers() {
            this.showMembersUpdating = true
            await this.teamStore.fetchMembers(+this.teamId!)
            this.showMembersUpdating = false
        },
        async refreshExpenses() {
            this.showExpensesUpdating = true
            await this.teamStore.fetchExpenses(+this.teamId!)
            this.showExpensesUpdating = false
        },
        refreshAll() {
            this.refreshMembers()
            this.refreshExpenses()
            this.newExpensesReceived = false
        },
        toggleMembersDetails() {
            this.membersDetailsShown = !this.membersDetailsShown
        },
        getOperationMembername(memberId: number) {
            const member = this.members.find(
                (member) => member.id == memberId
            ) as User
            return `${member?.firstName ?? ''} ${member?.lastName ?? ''}`
        },
        subscribeToOtherUsersActions() {
            this.socket = new WebSocket(
                api.getWebsocketUrl(`ws/team_expenses/${this.teamId}/`)
            )
            this.socket.addEventListener('message', this.onWebSocketMessage)
            this.socket.addEventListener('error', this.onWebSocketError)
        },
        sendWebsocketMessage() {
            if (this.socket && this.socket.readyState === WebSocket.OPEN) {
                this.socket!.send(
                    JSON.stringify({
                        sender:
                            this.user!.firstName + ' ' + this.user!.lastName,
                    })
                )
            }
        },
        onWebSocketMessage(event: any) {
            const message = JSON.parse(event.data)
            if (
                !this.newExpensesReceived &&
                message.sender !=
                    this.user!.firstName + ' ' + this.user!.lastName
            ) {
                this.addToast({
                    message: `${
                        message.sender ?? 'Someone'
                    } added a new expense or settled up. Click refresh button to see it or refresh the page.`,
                    type: 'success',
                })
                this.newExpensesReceived = true
            }
        },
        onWebSocketError(_: any) {
            this.addToast({
                message: "Couldn't refresh the expenses and members",
                type: 'danger',
            })
        },
    },
    computed: {
        membersWithoutUser() {
            //@ts-ignore
            return this.members.filter((member) => member.id !== this.user.id)
        },
        sumTheyOwe() {
            return this.membersWithoutUser.reduce((sum, member) => {
                return sum + (member.owesYou?.value ?? 0)
            }, 0)
        },
        sumYouOwe() {
            return this.membersWithoutUser.reduce((sum, member) => {
                return sum + (member.youOwe?.value ?? 0)
            }, 0)
        },
    },
})
</script>
