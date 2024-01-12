<template lang="pug">
.group-avatar.overflow-hidden
    .avatar-part(:style="partStyle(1)")
    .avatar-part(:style="partStyle(2)")
    .avatar-part(:style="partStyle(3)")
</template>

<script lang="ts">
import { Group } from '@/pages/split/types/group.types'
import { PropType, defineComponent } from 'vue'

export default defineComponent({
    name: 'GroupAvatar',
    props: {
        group: Object as PropType<Group>,
    },
    methods: {
        generateHash(str: string): number {
            let hash = 0
            for (let i = 0; i < str.length; i++) {
                hash = (hash << 5) - hash + str.charCodeAt(i)
                hash |= 0
            }
            return hash
        },
        getColor(hash: number, index: number): string {
            const hue = (hash + index * 100) % 360
            return `hsl(${hue}, 70%, 50%)`
        },
        partStyle(index: number): object {
            const angle = 120 * index
            const hash = this.generateHash(this.group!.name.toString() || '')
            const color = this.getColor(hash, index)
            return {
                clipPath: `polygon(50% 0%, 50% 50%, 100% 50%, 100% 0%, 50% 0%, 50% 50%, 0% 50%, 0% 0%)`,
                transform: `rotate(${angle}deg)`,
                backgroundColor: color,
            }
        },
    },
})
</script>

<style scoped>
.group-avatar {
    aspect-ratio: 1 / 1;
    height: 2.5rem;
    width: 2.5rem;
    border-radius: 50%;
    position: relative;
}

.avatar-part {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

</style>
