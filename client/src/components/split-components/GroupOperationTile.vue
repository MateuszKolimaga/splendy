<template lang="pug">
.card.my-3.overflow-hidden.border.border-1(style="cursor: pointer;" :class="valueYouAreOwed && !isSettledByThem ? 'border-success' : valueYouOwe && !isSettledByYou ? 'border-warning' : 'border-secondary'")
    .container-fluid.gx-0(@mouseover="handleMouseOver" @mouseleave="handleMouseLeave")
        .d-flex.flex-column
            .d-flex.flex-row.d-flex.bg-light.px-2.py-2.fw-light.align-items-center
                .w-100.px-2.d-flex.flex-row.gap-2.align-items-center(v-if="fromMember")
                    .fw-light.text-secondary(v-if="fromMember.id == user.id") You
                    user-avatar(v-else :user="fromMember" :size="`1.3rem`")
                    .fw-normal(v-if="showExtraInfo && fromMember.id !== user.id") {{ fromMember.firstName }} {{ fromMember.lastName }}
                    .fw-light.text-secondary paid
                    .fw-normal {{ groupOperation.value }} {{ groupOperation.currency }}
                    .fw-light.text-secondary ;
                    .d-flex.flex-row.gap-2(v-if="!showExtraInfo")
                        .fw-normal {{ membersAffected.length }}
                    .d-flex.flex-row.gap-2(v-else)
                        user-avatar(v-for="member in membersAffected" :key="member.id" :user="member" :size="`1.3rem`")
                    .fw-light.text-secondary(v-if="fromMember.id !== user.id") {{ membersAffected.length > 1 ? 'members owe a debt' : 'member owes a debt' }}
                    .fw-light.text-secondary(v-else) {{ membersAffected.length > 1 ? 'members owe you' : 'member owes you' }}
                button.btn-close.flex-shrink-1(v-if="showCloseButton && !isSettledByThem" @click="deleteGroupOperation" type="button" aria-label="Close" style="font-size: 12px; padding: 2px;")
                font-awesome-icon(v-else-if="fromMember && ((valueYouOwe && isSettledByYou) || (valueYouAreOwed && isSettledByThem))" icon="check" style="color: black")
            .d-flex.flex-row(:key="groupOperation.description", @click="handleGroupOperationClick")
                .col-1.pt-2.ps-3
                    date-component.mb-2(:date="groupOperation.date")
                .col-9.pt-4.pe-4.d-flex.flex-row.gap-2
                    | {{ groupOperation.description }}
                .col-2.p-3
                    .d-flex.flex-row-reverse.align-items-center
                        .d-flex.flex-column
                            .d-flex.flex-row.justify-content-end
                                .you-owe-info(v-if="valueYouOwe")
                                    .text-warning.text-opacity-75(v-if="!isSettledByYou") You owe
                                    .text-black.text-opacity-75(v-else) You paid
                                .you-are-owed-info(v-else-if="valueYouAreOwed")
                                    .text-success.text-opacity-75(v-if="!isSettledByThem") You are owed
                                    .text-black.text-opacity-75(v-else) Everyone paid
                                .you-are-were-involved-info(v-else)
                                    .text-muted.text-opacity-75 Not involved
                            .d-inline-flex.gap-2.d-flex.flex-row.justify-content-end(v-if="valueYouOwe || valueYouAreOwed")
                                .fw-bold(v-if="valueYouOwe") {{ valueYouOwe }}
                                .fw-bold(v-else) {{ valueYouAreOwed }}
                                | {{  groupOperation.currency }}
</template>

<script lang="ts">
import { PropType, defineComponent, ref } from 'vue'
import DateComponent from '../date/DateComponent.vue'
import { useUserStore } from '@/stores/userStore'
import { storeToRefs } from 'pinia'
import GroupOperation from '@/pages/split/models/groupOperations'
import UserAvatar from '../user/UserAvatar.vue'
import { useTeamStore } from '@/stores/teamStore'

export default defineComponent({
    name: 'GroupOperationTile',
    components: {
        DateComponent,
        UserAvatar
    },
    props: {
        groupOperation: Object as PropType<GroupOperation>,
    },
    setup(props) {
        const showExtraInfo = ref(false)
        const { user } = storeToRefs(useUserStore())
        const teamStore = useTeamStore()
        const { members } = storeToRefs(teamStore)
        const operationCost = props.groupOperation!.value!
        const numOfMembersAffected = props.groupOperation!.to_users.length
        const settledUsers = props.groupOperation!.users_settled
        const showCloseButton = ref(false)
        const shouldShowExtraInfo = ref(false)
        const loading = ref(false)
        const isSettledByYou = settledUsers.indexOf(+user.value?.id!) != -1
        const isSettledByThem = settledUsers.length == numOfMembersAffected
        return {
            showExtraInfo,
            shouldShowExtraInfo,
            showCloseButton,
            operationCost,
            numOfMembersAffected,
            user,
            members,
            teamStore,
            loading,
            settledUsers,
            isSettledByYou,
            isSettledByThem
        }
    },
    methods: {
        handleMemberClick() {
            this.$emit('groupOperation-click', this.groupOperation!.description)
        },
        async deleteGroupOperation() {
            this.loading = true
            await this.teamStore.deleteExpense(this.groupOperation!)
            this.loading = false
            
        },
        async handleMouseOver() {
            this.showCloseButton = this.groupOperation!.from_user == this.user!.id
            this.shouldShowExtraInfo = true
            await setTimeout(() => this.showExtraInfo = this.shouldShowExtraInfo, 800)
        },
        handleMouseLeave() {
            this.showCloseButton = false
            this.shouldShowExtraInfo = false
            this.showExtraInfo = false
        }
    },
    computed: {
        valueYouOwe() {
            if (this.user!.id != this.groupOperation!.from_user && this.groupOperation!.to_users.includes(+this.user!.id)) {
                return (this.operationCost/this.numOfMembersAffected).toFixed(2)
            } else {
                return 0
            }
        },
        valueYouAreOwed() {
            if (this.user!.id == this.groupOperation!.from_user) {
                return ((this.numOfMembersAffected -1)*this.operationCost/this.numOfMembersAffected).toFixed(2)
            }
            else return 0
        },
        membersAffected() {
            //@ts-ignore
            const members = this.members.filter(member => this.groupOperation!.to_users.includes(member.id) && member.id != this.groupOperation!.from_user)
            return members
        },
        fromMember() {
            const fromMember = this.members.filter(member => member.id == this.groupOperation!.from_user)[0]
            return fromMember
        }
    },
})
</script>


