import api from '@/common/api'
import { fakeL } from '@/common/locales'
import { useToasts } from '@/composables/useToasts'
import { defineStore } from 'pinia'
import { StoreResult } from './types'
import { anyKeysOfObject } from '@/utils/keys'
import { ref } from 'vue'
import { useUserStore } from './userStore'
import { useTeamStore } from './teamStore'
import { usePersonalStore } from './personalStore'

const { addToast } = useToasts()

export const useSignStore = defineStore('signStore', {
    state: () => ({
        storedEmail: '',
        loggedIn: ref(localStorage.getItem('token') !== null && true), //TODO: verif Token
    }),
    actions: {
        setStoredEmail(email: string) {
            this.storedEmail = email
        },
        setLoggedIn(status: boolean) {
            this.loggedIn = status
        },
        async signUp(
            email: string,
            firstName: string,
            lastName: string,
            password: string
        ): Promise<StoreResult> {
            if (
                email == '' ||
                firstName == '' ||
                lastName == '' ||
                password == ''
            ) {
                addToast({ message: fakeL('Fill all fields'), type: 'info' })
                return { success: false }
            }
            const response = await api.fetch('registration/', {
                method: 'POST',
                body: JSON.stringify({
                    email,
                    first_name: firstName,
                    last_name: lastName,
                    password1: password,
                    password2: password,
                }),
            })
            if (response.status === 201) {
                addToast({
                    message: fakeL('Verification email has been sent! Check your spam folder.'),
                    type: 'success',
                })
                return { success: true }
            } else if (response.status === 400) {
                if (response.data) {
                    if ('password1' in response.data) {
                        addToast({
                            message: 'Incorrect password', //response.data.password1[0],
                            type: 'danger',
                        })
                    } else if ('email' in response.data) {
                        addToast({
                            message: 'Incorect email', //response.data.email[0],
                            type: 'danger',
                        })
                    }
                    if (
                        anyKeysOfObject(
                            ['first_name', 'second_name'],
                            response.data
                        )
                    ) {
                        addToast({
                            message: fakeL('Wrong first or/and second name'),
                            type: 'danger',
                        })
                    }
                }
            } else if (response.status === 500) {
                addToast({
                    message: fakeL('Error occured on the server'),
                    type: 'danger',
                })
                return { success: false }
            }
            return { success: false }
        },
        async signIn(email: string, password: string): Promise<StoreResult> {
            if (email == '' || password == '') {
                addToast({ message: fakeL('Fill all fields'), type: 'info' })
                return { success: false }
            }
            const response = await api.fetch('auth/login/', {
                method: 'POST',
                body: JSON.stringify({
                    email,
                    password,
                }),
            })
            if (response.status === 400) {
                if (response.data) {
                    if (
                        anyKeysOfObject(['non_field_errors'], response.data)
                    ) {
                        addToast({
                            message:  'Incorrect email or password', //response.data.non_field_errors[0],
                            type: 'info',
                        })
                    } else if ('email' in response.data) {
                        addToast({
                            message: fakeL('E-mail is incorrect'),
                            type: 'danger',
                        })
                    }
                }
            } else if (response.status == 200) {
                localStorage.setItem('token', response.data.key)
                await useUserStore().setUser()
                this.setLoggedIn(true)
                if (sessionStorage.invitation) {
                    useTeamStore().handleInvitation(sessionStorage.invitation)
                }
                return { success: true }
            }
            return { success: false }
        },
        async signOut(): Promise<StoreResult> {
            await api.fetch('auth/logout/', {
                method: 'POST',
            }) //TODO: log if fail
            this.setLoggedIn(false)
            localStorage.removeItem('token')
            const userStore = useUserStore()
            userStore.unsetUser()
            const teamStore = useTeamStore()
            teamStore.unsetTeam()
            const personalStore = usePersonalStore()
            personalStore.unsetPersonal()
            return { success: true }
        },
    },
})
