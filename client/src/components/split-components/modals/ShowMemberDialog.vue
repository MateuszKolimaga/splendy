<template lang="pug">
.modal.fade#showMember(ref='showMemberRef')
  .modal-dialog.modal-dialog-centered.modal-sm
    .modal-content
      .modal-header
        h5.modal-title Settle up
        button.btn-close.flex-shrink-1(@click="closeModal" type="button" aria-label="Close")
      .modal-body.my-2
        .d-flex.flex-column
          .d-flex.flex-column.mb-2
            .d-flex.flex-row.justify-content-center
              UserAvatar(:user="member" :size="`5rem`")
            .text-center.mt-3 {{ member.firstName }} {{ member.lastName }}
            .text-center.text-muted.mt-1 {{ member.email }}
          .row.gx-1
            .col-12(v-if="member.youOwe")
              .card.p-2.bg-warning(@mouseover="showButtonInfo=true" @mouseleave="showButtonInfo=false")
                .d-flex.flex-column.gap-2
                    .amount.d-flex.flex-row.text-center.mx-auto.my-1
                      .text-white You owe
                      .fw-bold.text-white.mx-1 {{ member.youOwe.value.toFixed(2) }}
                      .text-white {{ member.youOwe.currency }}
                    button.btn.btn-light.text-nowrap.mx-4.mb-1(@click="executeModal")
                      .text(v-if="!loading") Settle up
                      .spinner-border.spinner-border-sm(v-else)
                    small.text-white.m-auto.px-2.text-center(v-if="showButtonInfo") Click this only if you transferred money to this person
            .col-12(v-else-if="member.owesYou")
              .card.p-2.bg-success(@mouseover="showButtonInfo=true" @mouseleave="showButtonInfo=false")
                .d-flex.flex-column.gap-2
                    .amount.d-flex.flex-row.text-center.mx-auto.my-1
                      .text-white Owes you
                      .fw-bold.text-white.mx-1 {{ member.owesYou.value.toFixed(2) }}
                      .text-white {{ member.owesYou.currency }}
                    button.btn.btn-light.text-nowrap.mx-4(@click="executeModal") 
                      .text(v-if="!loading") Remind
                      .spinner-border.spinner-border-sm(v-else)
                    small.text-white.m-auto.px-2.text-center(v-if="showButtonInfo") This will send a reminder email
            .col-12(v-else)
              .card.p-2.bg-secondary.my-1
                .d-flex.flex-column.gap-2
                    .amount.d-flex.flex-row.text-center.mx-auto.my-1
                      .text-white Settled up
</template>
  


<script lang="ts">
//TODO: Add attachment to dialog
import { PropType, defineComponent, ref } from 'vue';
import UserAvatar from '@/components/user/UserAvatar.vue';
import { Modal } from 'bootstrap'
import { useTeamStore } from '@/stores/teamStore';
import { Member } from '@/pages/split/types/member';

export default defineComponent({
    name: "ShowMemberDialog",
    props: {
      member: Object as PropType<Member>
    },
    components: {
      UserAvatar
    },
    methods: {
      async executeModal() {
        this.loading = true
        if(this.member!.youOwe) {
          await this.teamStore.settleUpWithUser([this.member!])
        } else {
          await this.teamStore.sendDebtReminder(this.member!.email.valueOf())
        }
        this.$emit('execute')
        this.closeModal()
      },
      closeModal() {
        this.loading = false
        this.showMember?.dispose()
        this.$emit('close')
      },
    },
    setup() {
        const showMember = ref<Modal>()
        const showMemberRef = ref()
        const showButtonInfo = ref(false)
        const loading = ref(false)
        const teamStore = useTeamStore()
        return {
          showMemberRef,
          showMember,
          showButtonInfo,
          loading,
          teamStore
        }
    },
    mounted() {
      this.showMember = new Modal(this.showMemberRef)
      this.showMemberRef.addEventListener('hidden.bs.modal', () => {
          this.closeModal()
      })
      this.showMember.show();
    },
    
  });
</script>

<style scoped lang="scss">
.btn-light {
    &:hover {
        background-color: #f0f2f5 !important;
    }
}
</style>