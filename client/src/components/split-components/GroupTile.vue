<template lang="pug">
.item-row(@click="handleGroupClick")
    .item-body.mb-2(:key="group.id")
        GroupAvatar(:group="group")
        | {{ group.name }}
</template>

<script lang="ts">
import { PropType, defineComponent } from 'vue';
import { Group } from '@/pages/split/types/group.types';
import GroupAvatar from '../group/GroupAvatar.vue';

export default defineComponent({
    name: "GroupTile",
    components: {
        GroupAvatar
    },
    props: {
        group: Object as PropType<Group>
    },
    methods: {
        handleGroupClick() {
            this.$emit('group-click', this.group!.id)
        }
    }
})
</script>

<style scoped lang="scss">
@import '@/styles/styles.scss';

.item-row {
display: flex;
flex-direction: row;
margin: 0 1rem 0 1rem;
}

.item-body {
    padding: 1rem 1.5rem 1rem 1.5rem; /* Increase padding for a less crowded look */
    display: flex;
    width: 100%;
    justify-content: start;
    background-color: white;
    align-items: center;
    font-weight: bold;
    border-radius: 10px;
    border: 1px solid $almost-non-existent-grey;
    /* color: white; */
    gap: 1rem;
    cursor: pointer;
}
</style>