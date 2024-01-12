<template lang="pug">
.d-flex.flex-row.px-2(@mouseover="handleMouseOver" @mouseleave="handleMouseOut" style={'cursor': 'pointer'})
  .card.overflow-x-hidden.rounded.my-2.flex-fill.align-self-center
    .d-flex.flex-row
      .flex-shrink-1.p-2(:style="{ 'background-color': operationCategoryInfos[operation.category].color }")
      .w-100.me-5.py-2
        .d-flex.align-items-center
          .col-1.ps-4.me-4
            DateComponent(:date = "operation.date")
          .col-8.px-2 {{ operation.description }}
          .col-2.text-end.fw-bold {{operation.value.toFixed(2)}}
          .col-1.flex-grow-1.ms-3 {{operation.currency}}
  .close-button.flex-shrink-1.d-flex.flex-column.justify-content-center.mx-2
    button.btn.btn-sm.flex-shrink-1.me-2(@click="deleteOperation" type="button" aria-label="Close" v-if="isCardHovered && showCloseButton && !deletingOperation")
      font-awesome-icon(icon="trash")
    template(v-if="isCardHovered && showCloseButton && deletingOperation")
      .spinner-border.spinner-border-sm.ms-1.me-3(role="status", style="color: grey")  
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { operationCategoryInfos } from '../../pages/dashboard/models/operation-infos'
import { useDateFormatter } from '../../composables/date/dateFormatter'
import DateComponent from '../../components/date/DateComponent.vue'
import { usePersonalStore } from '@/stores/personalStore'

export default defineComponent({
    name: 'OperationTile',
    components: {
        DateComponent,
    },
    props: {
        operation: Object,
    },
    data() {
        return {
            operationCategoryInfos,
            isCardHovered: false,
            showCloseButton: false,
        }
    },
    setup() {
        const { formatDateTime } = useDateFormatter()
        const isCardHovered = ref(false)
        const showCloseButton = ref(false)
        const shouldShowCloseButton = ref(true)
        const deletingOperation = ref(false)
        const personalStore = usePersonalStore()

        const handleMouseOver = () => {
            isCardHovered.value = true
            shouldShowCloseButton.value = true
            setTimeout(() => {
                showCloseButton.value = shouldShowCloseButton.value
            }, 800)
        }

        const handleMouseOut = () => {
            isCardHovered.value = false
            showCloseButton.value = false
            shouldShowCloseButton.value = false
        }

        return {
            formatDate: (date: Date) => formatDateTime(date),
            isCardHovered,
            showCloseButton,
            personalStore,
            handleMouseOver,
            handleMouseOut,
            deletingOperation,
        }
    },
    methods: {
        deleteOperation() {
            this.deletingOperation = true
            this.$emit('delete-operation', this.operation)
        },
    },
})
</script>

<style scoped>
.card:hover {
    border: 1px solid grey;
}
</style>
