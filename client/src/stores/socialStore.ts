import api from '@/common/api'
import { defineStore } from 'pinia'


export const useSocialStore = defineStore('social', {
    state: () => ({
        teams: [],
    }),
    persist: {
        storage: sessionStorage
    },
    actions: {
        async fetchTeams() {
            const response = await api.fetch('teams/')
            this.teams = response.data.results.sort((a: { created_date: string }, b: { created_date: string }) => {
                return new Date(b.created_date).getTime() - new Date(a.created_date).getTime()
            })
            return { success: true }
        },
        async createTeam(form: any) {
            const response = await api.fetch('teams/', {method: 'POST', body: JSON.stringify(form)})
            await this.fetchTeams()
            return { success: true, message: response.data }
        }
    },
})
