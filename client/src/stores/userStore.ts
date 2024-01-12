import api from '@/common/api'
import { useToasts } from '@/composables/useToasts'
import { defineStore } from 'pinia'
import { StoreResult } from './types'
import { User } from '@/pages/split/types/user'
const { addToast } = useToasts()

export const useUserStore = defineStore('userStore', {
    state: () => ({
        user: <User | null>(null),
    }),
    persist: {
        storage: localStorage
    },
    actions: {
        async setUser(): Promise<StoreResult> {
            const response = await api.fetch('auth/user', {
                method: 'GET',
            })
            const apiUser = response.data
            this.user = new User(apiUser.pk, apiUser.email, apiUser.first_name, apiUser.last_name, apiUser.currency,  apiUser.avatar,)
            return { success: true }
        },
        unsetUser(): StoreResult {
            this.user = null;
            return { success: true }
        },
        async updateUser(newUser: User) {
            const response = await api.fetch(`auth/user/`, {
                method: 'PUT',
                body: User.toJson(newUser)
            })
            if (response.status == 200) {
                await this.setUser()
                addToast({
                    message: 'Updated successfully',
                    type: 'success',
                })
            } else {
                addToast({message: 'Error while updating user', type: 'danger'})
            }
        }
    },
})
