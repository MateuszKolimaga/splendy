<template lang="pug">
.container-fluid.gx-0
    .row.d-flex.gx-0
        .group-panel.fixed-h.col-4.bg-light.p-0.border-end.d-flex.flex-column
            .panel-header.p-4.bg-light.border.border-end-0
                .d-flex.align-items-center
                    .flex-grow-1.ms-3 
                        .d-flex.flex-row.fw-bold.align-items-center
                            .text Groups
                            .spinner-border.spinner-border-sm.ms-2(v-if="showSpinner")
                    .ms-3
                        button.btn.btn-primary(@click="openAddGroupDialog")
                            font-awesome-icon(icon="plus" style={'color': 'white'})
            .panel-body.overflow-y-auto.flex-grow-1.pt-3(v-if="showSpinner")
                .d-flex.flex-column.align-items-center.justify-content-center.h-100
                    .text-muted.mt-2 Fetching members...
            .panel-body.overflow-y-auto.flex-grow-1.pt-3(v-else-if="groups.length > 0")
                GroupTile.my-1(v-for="group in groups" , :key="group.id", :group="group", @group-click="handleGroupClick")
            .panel-body.overflow-y-auto.flex-grow-1.pt-3(v-else)
                .d-flex.flex-column.align-items-center.justify-content-center.h-100
                    .text-muted No groups yet
                    .text-muted.mt-2(@click="openAddGroupDialog" style="cursor: pointer;") Create a group to start splitting the bills
        .center-panel.col-8.fixed-h.bg-light.border-top.d-flex.align-items-center
            .d-flex.flex-column.w-100
                .row.d-flex.flex-row.flex-wrap
                    .col-4
                        .d-flex.flex-row.justify-content-stretch.ms-2
                            content-card.mx-3(:image="images.teamImage1", :title="`Create a group`", @click="openAddGroupDialog", style="cursor: pointer;")
                    .col-4
                        .d-flex.flex-row.justify-content-stretch
                            content-card.mx-3(:image="images.teamImage2", :title="`Invite friends`", @click="openAddGroupDialog", style="cursor: pointer;")
                    .col-4
                        .d-flex.flex-row.justify-content-stretch.me-2
                            content-card.mx-3(:image="images.teamImage3", :title="`Split the bills`", @click="openAddGroupDialog", style="cursor: pointer;")
                .d-flex.flex-row.align.justify-content-center.mt-5
                    button.btn.btn-lg.btn-primary.m-4(@click="openAddGroupDialog") Create a group
AddGroupDialog(v-if="isAddGroupDialogOpen", @close="closeAddGroupDialog")
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import ChartComponent from '@/components/chart/pie/ChartComponent.vue'
import GroupTile from '@/components/split-components/GroupTile.vue'
import teamImage1 from '../../assets/team/team1.svg'
import teamImage2 from '../../assets/team/team2.svg'
import teamImage3 from '../../assets/team/team3.svg'
import AddGroupDialog from '@/components/split-components/modals/AddGroupDialog.vue'
import ContentCard from '@/components/cards/ContentCard.vue'
import { storeToRefs } from 'pinia'
import { useSocialStore } from '@/stores/socialStore'


export default defineComponent({
    name: 'SocialSplitPage',
    components: {
        ChartComponent,
        GroupTile,
        AddGroupDialog,
        ContentCard,
    },
    setup() {
        const isAddGroupExpenseDialogOpen = ref(false)
        const isAddGroupDialogOpen = ref(false)
        const socialStore = useSocialStore()
        const { teams } = storeToRefs(socialStore)
        const showSpinner = ref(teams.value.length == 0)
        socialStore.fetchTeams().then(() => showSpinner.value = false)
        return {
            socialStore,
            groups: teams,
            isAddGroupExpenseDialogOpen,
            isAddGroupDialogOpen,
            showSpinner
        }
    },
    methods: {
        handleGroupClick(groupId: number) {
            this.$router.push(`/split-dashboard/${groupId}`)
        },
        openAddGroupExpenseDialog() {
            this.isAddGroupExpenseDialogOpen = true
        },
        closeAddGroupExpenseDialog() {
            this.isAddGroupExpenseDialogOpen = false
        },
        openAddGroupDialog() {
            this.isAddGroupDialogOpen = true
        },
        closeAddGroupDialog() {
            this.isAddGroupDialogOpen = false
        },
    },
    data() {
        return {
            images: {
                teamImage1,
                teamImage2,
                teamImage3,
            },
        }
    },
})
</script>

<style scoped>
.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
