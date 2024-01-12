<template lang="pug">
.modal.fade#addMember(ref="addMemberRef")
  .modal-dialog.modal-dialog-centered
    .modal-content
      .modal-header
          h5.modal-title Invite a member
          button.btn-close.flex-shrink-1(@click="closeModal" type="button" aria-label="Close")
      .modal-body.my-2
        .form-group(v-if="selectedFriend === null")
          label.mb-2.ms-1(for="emailInput") Invite via email
          input#emailInput.form-control(v-model="emailInput" type="email" placeholder="Enter email")
        .form-group(v-if="emailInput === '' && friends.length > 0")
          label.mb-2.ms-1(for="friendDropdown") Or choose your friend
          select#friendDropdown.form-control(v-if="!loadingFriends" v-model="selectedFriend")
            option(v-for="friend in friends" :key="friend.id" :value="friend") {{ `${friend.first_name} ${friend.last_name}` }}
          .d-flex.flex-row.align-items-center.w-100.justify-content-center(v-else)
            .spinner-border.spinner-border-sm

      .modal-footer
        button.btn.btn-md.btn-outline-secondary.mx-3(@click="closeModal") Cancel
        button.btn.btn-md.btn-primary(@click="executeModal", :disabled="isLoading") 
            .text(v-if="!isLoading") Invite
            span.spinner-border.spinner-border-sm(v-else, role="status", aria-hidden="true")
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { Modal } from 'bootstrap'
import { useUserStore } from '@/stores/userStore'
import { useToasts } from '@/composables/useToasts'
import { useTeamStore } from '@/stores/teamStore'

export default defineComponent({
    name: 'AddMemberDialog',
    props: {
        friends: Array,
    },
    data() {
        return {
            selectedFriend: null,
            emailInput: '',
        }
    },
    setup(props) {
        const addMember = ref<Modal>()
        const addMemberRef = ref()
        const userStore = useUserStore()
        const teamStore = useTeamStore()
        const isLoading = ref(false)
        const { addToast } = useToasts()
        const friends = ref(props.friends)
        const loadingFriends = ref(true)
        if (!props.friends) {
            teamStore.fetchFriends().then(
                (result) => {
                    friends.value = result.message
                    loadingFriends.value = false
                }
            )
        } else {
            loadingFriends.value = false
        }
        return {
            addMember,
            addMemberRef,
            userStore,
            teamStore,
            isLoading,
            addToast,
            friends,
            loadingFriends
        }
    },
    methods: {
        async executeModal() {
            this.isLoading = true
            if (this.emailInput !== '') {
                await this.teamStore.sendTeamInvitation(this.emailInput)
                this.$emit('email', this.emailInput)
                this.closeModal()
            } else if (this.selectedFriend !== null) {
                //@ts-ignore
                await this.teamStore.sendTeamInvitation(this.selectedFriend.email)
                this.$emit('friend', this.selectedFriend)
                this.closeModal()
            } else {
                this.closeModal()
            }
        },
        closeModal() {
            this.isLoading = false
            this.addMember?.dispose()
            this.$emit('close')
        },
    },
    mounted() {
        this.addMember = new Modal(this.addMemberRef)
        this.addMemberRef.addEventListener('hidden.bs.modal', () => {
            this.closeModal()
        })
        this.addMember.show()
    },
})
</script>

<style scoped lang="scss">
.form-group {
    margin-bottom: 15px;
}
</style>
