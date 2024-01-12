<template lang="pug">
.chat-container.bg-light.border.border-success
    .messages-header.d-flex.flex-row-reverse
        button.btn-close.flex-shrink-1(type="button" aria-label="Close", @click="close")
    .chat-messages(ref="chatMessagesRef")
        .d-flex.flex-column.align-items-center.justify-content-center.h-100(v-if="fetchingMessages")
            .spinner-border
        .d-flex.flex-column.align-items-center.justify-content-center.h-100(v-else-if="dbMessages.length === 0 && socketMessages.length === 0")
            .message-sender.text-muted.text-opacity-75 Type your first message to the group
        .div(v-else)
            .card.message.bg-white.p-2.mx-2(v-for="(message, index) in dbMessages" :key="index" :style="{'background-color': switchMessageColor(message)}")
                //- .message-separator(v-if="index > 0 && shouldShowSeparator(dbMessages[index - 1].timestamp, message.timestamp)")
                //-     | {{ formatDateSeparator(message.timestamp) }}
                .d-flex.flex-row.gap-2.align-items-center
                    .message-sender.ms-2 {{ getSenderName(message.user) }}
                    .message-time.text-muted.text-opacity-75.ms-1 {{ formatTime(message.timestamp) }}
                .message-content.my-2 {{ message.text }}
            .card.message.bg-white.p-2.mx-2(v-for="(message, index) in socketMessages" :key="index" :style="{'background-color': switchMessageColor(message)}")
                //- .message-separator(v-if="index > 0 && shouldShowSeparator(dbMessages[index - 1].timestamp, message.timestamp)")
                //-     | {{ formatDateSeparator(message.timestamp) }}
                .d-flex.flex-row.gap-2.align-items-center
                    .message-sender.ms-2 {{ message.sender }}
                    .message-time.text-muted.text-opacity-75.ms-1 {{ formatTime(message.timestamp) }}
                .message-content.my-2 {{ message.message }}
    .d-flex.flex-row.mt-2.align-items-center.gap-3
        input#messageInput.form-control.mx-2(v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message...")
        font-awesome-icon.flex-shrink-1.pe-3(v-if="canSend" icon='paper-plane', @click="sendMessage", style="cursor: pointer")
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { Message } from '@/pages/split/types/message.types'
import { storeToRefs } from 'pinia'
import { useTeamStore } from '@/stores/teamStore'
import api from '@/common/api'
import { useUserStore } from '@/stores/userStore'
import { useToasts } from '@/composables/useToasts'

export default defineComponent({
    name: 'ChatComponent',
    props: {
        groupId: String,
    },
    setup(props) {
        const teamStore = useTeamStore()
        const userStore = useUserStore()
        const fetchingMessages = ref(true)
        const dbMessages = storeToRefs(teamStore).messages
        const members = teamStore.members
        const isChatOpen = ref(true)
        const canSend = ref(false)
        const socketMessages = ref([])
        const chatMessagesRef = ref<HTMLElement | null>(null)
        
        teamStore.fetchMessages(props.groupId!).then(() => {
            fetchingMessages.value = false
        })
        const { addToast } = useToasts()
        return { fetchingMessages, isChatOpen, chatMessagesRef, canSend, members, userStore, dbMessages, socketMessages, addToast}
    },
    data() {
        const socket = ref<WebSocket | null>(null)
        return {
            newMessage: '',
            socket
        }
    },
    mounted() {
        this.scrollToBottom()
        this.connectWebSocket()
    },
    methods: {
        async sendMessage() {
            if (this.newMessage.trim() !== '') {
                if (this.socket && this.socket.readyState === WebSocket.OPEN) {
                    this.socket.send(JSON.stringify({
                        sender: this.getSenderName(this.userStore.user!.id.valueOf()),
                        message: this.newMessage,
                    }))
                }
                
                this.newMessage = ''
                setTimeout(() => {
                    this.scrollToBottom()
                }, 100)
            }
        },
        scrollToBottom() {
            if (this.chatMessagesRef) {
                this.chatMessagesRef.scrollTop =
                    this.chatMessagesRef.scrollHeight
            }
        },
        switchMessageColor(message: Message & {'sender': string, 'message': string}) {
            const sender = message.user ? this.getSenderName(message.user) : message.sender

            let hash = 0
            for (let i = 0; i < sender.length; i++) {
                hash = sender.charCodeAt(i) + ((hash << 5) - hash)
            }

            const hue = Math.abs(hash) % 360
            const saturation = 80
            const lightness = 90

            const color = `hsl(${hue}, ${saturation}%, ${lightness}%)`
            return color + ' !important'
        },
        getSenderName(user_id: number) {
            const user = this.members.find((member) => member.id === user_id)
            return user!.firstName + ' ' + user!.lastName
        },
        connectWebSocket() {
            this.socket = new WebSocket(api.getWebsocketUrl(`ws/chat/${this.groupId}/`))
            this.socket.addEventListener('message', this.onWebSocketMessage)
            this.socket.addEventListener('error', this.onWebSocketError)
        },
        onWebSocketMessage(event: any) {
            const message = JSON.parse(event.data)
            //@ts-ignore
            this.socketMessages.push({
                sender: message.sender,
                message: message.message,
                timestamp: message.timestamp
            })
            setTimeout(() => {
                    this.scrollToBottom()
                }, 100)
        },
        onWebSocketError(_: any) {
            this.addToast({ message: 'Couldn\'t refresh the chat', type: 'danger'})
        },
        formatTime(timestamp: string): string {
            const date = new Date(timestamp);
            const day = date.getDate().toString().padStart(2, '0');
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            return `${month}-${day} ${hours}:${minutes}`;
        },

        shouldShowSeparator(prevTimestamp: string, currentTimestamp: string): boolean {
            const prevDate = new Date(prevTimestamp);
            const currentDate = new Date(currentTimestamp);

            return prevDate.getDate() !== currentDate.getDate();
        },

        formatDateSeparator(timestamp: string): string {
            const date = new Date(timestamp);
            const day = date.getDate().toString().padStart(2, '0');
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            return `${day}-${month}`;
        },

        close() {
            this.$emit('close')
        },
    },
    watch: {
        newMessage() {
            if (this.newMessage.trim() !== '') {
                this.canSend = true
            } else {
                this.canSend = false
            }
        },
        fetchingMessages () {
            if (!this.fetchingMessages) {
                setTimeout(() => {
                    this.scrollToBottom()
                }, 300)
            }
        }
    },
})
</script>

<style scoped lang="scss">
.chat-container {
    width: 40%;
    margin: 20px;
    padding: 10px;
    position: fixed;
    bottom: 0px;
    right: 0px;
    z-index: 1000;
}
.chat-messages {
    height: 300px;
    overflow-y: auto;
    border-bottom: 1px solid #ccc;

    .message {
        margin: 10px 0;
    }

    .message-sender {
        font-weight: bold;
    }

    .message-content {
        margin-left: 10px;
    }
}

.chat-input {
    margin-top: 10px;
}

.message-time {
    font-size:x-small;
}
</style>
