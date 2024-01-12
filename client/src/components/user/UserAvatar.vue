<template lang="pug">
.user-avatar(v-if="user?.avatar" :style="{ height: size, width: size }")
    img(:src="user?.avatar" alt="User Avatar" class="avatar-img")
.avatar-initials(v-else :style="avatarBackgroundStyle") 
    .text.fw-bold(:style="textStyle") {{ avatarInitials }}
</template>

<script lang="ts">
import { useUserStore } from '@/stores/userStore'
import { storeToRefs } from 'pinia'
import { defineComponent, ref } from 'vue'

export default defineComponent({
    name: 'UserAvatar',
    props: {
        size: {
            type: String,
            default: '2.5rem'
        },
        user: Object,
    },
    setup(props) {
        const user = props.user ? props.user : storeToRefs(useUserStore()).user
        return { user, avatarInitials: ref('') }
    },
    computed: {
        avatarBackgroundStyle() {
            if (!this.user?.avatar && this.user) {
                this.avatarInitials =
                    this.user.firstName.charAt(0).toUpperCase() +
                    this.user.lastName.charAt(0).toUpperCase()
                var firstColor =
                    avatarColors[(this.avatarInitials.charCodeAt(0) - 65) % 19]
                var secondColor =
                    avatarColors[
                        (this.avatarInitials.charCodeAt(1) - 65 + 2) % 19
                    ]
                return `background: linear-gradient(135deg, ${firstColor} 50%, ${secondColor} 50%); height: ${this.size}; width: ${this.size}`
            }
        },
        textStyle() {
            if (!this.user?.avatar && this.user) {
                const fontSize = parseFloat(this.size) / 2.5
                return {
                    fontSize: `${fontSize}rem`
                }
            }
        }
    },
})

const avatarColors = [
    '#1abc9c',
    '#2ecc71',
    '#3498db',
    '#9b59b6',
    '#34495e',
    '#16a085',
    '#27ae60',
    '#2980b9',
    '#8e44ad',
    '#2c3e50',
    '#f1c40f',
    '#e67e22',
    '#e74c3c',
    '#95a5a6',
    '#f39c12',
    '#d35400',
    '#c0392b',
    '#bdc3c7',
    '#7f8c8d',
]
</script>

<style scoped>
.user-avatar {
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    overflow: hidden;
    position: relative;
}

.avatar-initials {
    height: 2.5rem;
    width: 2.5rem;
    font: 1rem Arial;
    color: white;
    text-align: center;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-size: 200% 100%;
    transition: background-position 0.5s ease;
}
.avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

.text {
    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
    -khtml-user-select: none; /* Konqueror HTML */
    -moz-user-select: none; /* Old versions of Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
}
</style>
