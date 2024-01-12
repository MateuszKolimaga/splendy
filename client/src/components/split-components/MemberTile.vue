<template lang="pug">
.card.mt-3.mx-3.border.border-1(@mouseover="memberHover" @mouseleave="memberUnhover" @click="handleMemberClick" style="cursor: pointer" :class="member.youOwe ? 'border-warning' : (member.owesYou ? 'border-success' : 'border-secondary') ")
    .short-user-info.bg-warning(v-if="member.youOwe")
        .ps-3.d-flex.flex-row.align-items-center.justify-content-between(v-if="memberHovered || showDetails")
            .d-flex.flex-row.align-items-center
                .text-white You owe 
                .text-white.fw-bold.mx-1 {{ member.youOwe?.value.toFixed(2) }} 
                .text-white {{ member.youOwe?.currency }}
            .text-white.fw-bold.mx-3.my-1  Click to settle up
    .short-user-info.bg-success(v-else-if="member.owesYou")
        .ps-3.d-flex.flex-row.align-items-center.justify-content-between(v-if="memberHovered || showDetails")
            .d-flex.flex-row.align-items-center
                .text-white.ps-2 Owes you 
                .text-white.fw-bold.px-1 {{ member.owesYou?.value.toFixed(2) }} 
                .text-white {{ member.owesYou?.currency }}
            .text-white.fw-bold.mx-3.my-1 Click to remind
    .short-user-info.bg-secondary(v-else)
        .ps-3.d-flex.flex-row.align-items-center.justify-content-between(v-if="memberHovered || showDetails")
            .d-flex.flex-row.align-items-center
                .text-white.ps-1.my-1 No debts
    .d-flex.flex-column
        .item-body.rounded.px-1.py-3.mx-3
            .user-info.d-flex.flex-row.w-100.align-items-center.gap-2.justify-content-between
                .d-flex.flex-row.align-items-center.gap-2
                    UserAvatar(:user="member")
                    .member-name.ms-1 {{ member.firstName }} {{ member.lastName }}
                font-awesome-icon(v-if="!member.youOwe && !member.owesYou" icon="check")
    
show-member-dialog(v-if="isDialogOpen" :member="member" @execute="handleSettleUp" @close="closeModal")
</template>
    
<script lang="ts">
import { PropType, defineComponent, reactive, ref } from 'vue';
import ShowMemberDialog from './modals/ShowMemberDialog.vue';
import UserAvatar from '../user/UserAvatar.vue';
import { Member } from '@/pages/split/types/member';
import { storeToRefs } from 'pinia';
import { useTeamStore } from '@/stores/teamStore';

export default defineComponent({
    name: "MemberTile",
    emits: ['settle-up'],
    components: {
        UserAvatar,
        ShowMemberDialog
    },
    props: {
        member: Object as PropType<Member>,
        showDetails: {
            type: Boolean, default: false
        }
    },
    methods: {
        handleMemberClick() {
            this.isDialogOpen = true
        },
        closeModal() {
            this.isDialogOpen = false
        },
        memberHover() {
            this.memberHovering = true;
            setTimeout(() => this.memberHovered = this.memberHovering, 400);
        },
        memberUnhover() {
            this.memberHovering = false;
            this.memberHovered = false
        },
        handleSettleUp() {
            this.$emit('settle-up', this.member)
        }
    },
    setup() {
        const isDialogOpen = ref(false);
        const memberHovered = ref(false);
        const memberHovering = ref(false);
        const userStore = useTeamStore()
        const { currency } = storeToRefs(userStore)
        const form = reactive({
            value: 0,
            description: "",
            category: "",
            currency: currency.value,
            isCyclic: false,
            cycleType: "days",
            cyclePeriod: 0,
            });
        return {
            isDialogOpen,
            form,
            memberHovered,
            memberHovering
        }
    }
})
</script>

<style scoped lang="scss">
.card {
    background-color: white;
    // border: 1px solid grey !important;
    overflow: hidden;

    &:last-child {
    margin-bottom: 0 !important;
    }
}

.member-balance {
    display: flex;
    flex-direction: row;
    justify-content: center;
    font-weight: normal;
    font-size: small;
    margin: auto;
    width: 100%;
    gap: 0.5rem;
    flex-wrap: wrap;

    .you-owe {
        color: red;
    }

    .owes-you {
        color: green;
    }
}

.fade-enter-active {
  transition: opacity 0.5s;
}

.fade-enter-from {
    opacity: 0;
}

.fade-leave-active {
  transition: opacity 0.001s;
}

.fade-leave-to {
  opacity: 0;
}

.btn-light {
    &:hover {
        background-color: #f0f2f5 !important;
    }
}
</style>