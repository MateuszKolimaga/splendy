<template lang="pug">
header.bg-white.w-100(v-if="showHeader")
  .container-fluid.gx-0.px-4
    nav.navbar.navbar-expand-sm.g-0
        a.navbar-brand(href="/")
          img(:src="images.logo" alt="Splendy" width="100" height="65")
        button.navbar-toggler#navbar(type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" style="border: none !important")
          span.navbar-toggler-icon.text-dark
        .collapse.navbar-collapse.bg-white#navbarNav
            .navbar-options
              ul.custom-navbar-nav.navbar-nav.d-flex.align-items-center
                li.nav-item.mx-2(v-if="loggedIn")
                  a.nav-link.align-items-center.simple-nav-item(:href="'/dashboard'") Dashboard
                li.nav-item.mx-2(v-if="loggedIn")
                  a.nav-link.align-items-center.simple-nav-item(:href="'/split-social'") Split the bills
                li.nav-item.mx-1(v-if="!loggedIn")
                  a.nav-link.align-items-center.simple-nav-item.text-black(@click="isDemoOpen=true" style="cursor: pointer;") Show demo
                li.nav-item.mx-1(v-if="!loggedIn")
                  a.nav-link.align-items-center.simple-nav-item(:href="'/login'")
                    button.btn.btn-md.btn-outline-secondary Login
                li.nav-item.mx-2(v-if="!loggedIn")
                  a.nav-link.align-items-center.simple-nav-item(:href="'/sign-up'") 
                    button.btn.btn-md.btn-primary Sign up
                li.nav-item.ms-2(v-if="loggedIn")
                  .card.py-1.px-2.pointer(data-bs-toggle="dropdown")
                    .dropdown
                        user-avatar(style="cursor: pointer")
                    .dropdown-menu(:style="menuStyle")
                      .dropdown-header First name
                      .dropdown-item
                        .d-flex.flex-row.align-items-center(@click="startEditing")
                          font-awesome-icon.dropdown-icon(icon="edit")
                          .w-100 {{ user.firstName }}
                      .dropdown-header Last name
                      .dropdown-item
                        .d-flex.flex-row.align-items-center(@click="startEditing")
                          font-awesome-icon.dropdown-icon(icon="edit")
                          .w-100 {{ user.lastName }}
                        //-.dropdown-header Currency
                        //- .dropdown-item
                        //-  .d-flex.flex-row.align-items-center(@click="startEditing")
                        //-    font-awesome-icon.dropdown-icon(icon="chevron-down")
                        //-    .w-100 {{ user.currency }}
                      .dropdown-divider
                      .dropdown-item.text-danger(@click="signOut", style="cursor: pointer") Sign out
demo-dialog(v-if="isDemoOpen" @close="isDemoOpen=false")
change-user(v-if="isEditing" @close="isEditing = false" @execute="saveEdited")
</template>

<script lang="ts">
import { ref } from 'vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import logo from '../../assets/logo-transparents.svg'
import { useSignStore } from '@/stores/signStore'
import { useRouter } from 'vue-router'
import UserAvatar from '../user/UserAvatar.vue'
import { useUserStore } from '@/stores/userStore'
import ChangeUser from '../split-components/modals/ChangeUser.vue'
import { storeToRefs } from 'pinia'
import DemoDialog from '../dashboard-components/modals/DemoDialog.vue'

export default {
    name: 'MainHeaderComponent',
    components: {
        UserAvatar,
        ChangeUser,
        DemoDialog
    },
    setup() {
        const router = useRouter()
        const signStore = useSignStore()
        const { loggedIn } = storeToRefs(signStore)
        const userStore = useUserStore()
        const { user } = storeToRefs(userStore)

        const images = ref({
            logo: logo,
        })

        const showHeader = ref(true)
        const isEditing = ref(false)
        const isDemoOpen = ref(false)

        const signOut = async () => {
            await signStore.signOut()
            await router.push({ name: 'Home' })
            location.reload()
        }

        const startEditing = () => {
            isEditing.value = true
        }

        const saveEdited = async () => {
            isEditing.value = false
        }

        return {
            images,
            showHeader,
            loggedIn,
            signOut,
            user,
            startEditing,
            isEditing,
            saveEdited,
            isDemoOpen
        }
    },
    computed: {
        menuStyle(): string {
            const nameLength = Math.max(
                this.user?.firstName.length ?? 0,
                this.user?.lastName.length ?? 0
            )
            const basePadding = -6.5
            const computedPadding =
                nameLength > 10 ? -6.5 - (nameLength - 10) * 0.33 : basePadding
            return `margin-left: ${computedPadding}rem;`
        },
    },
}
</script>

<style lang="scss" scoped>
@import '@/styles/styles.scss';
@import '@/styles/custom-bootsrap.scss';

header {
    position: sticky;
    top: 0;
    z-index: 999;
    height: $header-h;

    @media (max-width: $xs) {
        position: static;
        height: 0;
    }
}

.container-fluid {
    @media (min-width: $xs) {
        // overflow: hidden;
    }

    @media (max-width: $xs) {
        height: 0;
    }
}

nav {
    height: $header-h;

    @media (max-width: $xs) {
        // height: 0;
    }
}

#navbarNav {
    @media (max-width: $xs) {
        background-color: #fff;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
    }

    @media (min-width: $xs) {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
    }
}

.navbar-options {
    align-items: center;

    @media (max-width: $xs) {
        display: flex;
        flex-direction: row;
        justify-content: center;
    }
}

.navbar-toggler:focus,
.navbar-toggler:active,
.navbar-toggler-icon:focus {
    outline: none;
    box-shadow: none;
}

.dropdown-header {
    padding: 0.2rem 1rem 0.2rem 0.7rem !important;
}

.dropdown-icon {
    color: grey;
    height: 0.7rem;
    width: 0.7rem;
    padding: 0 0.5rem 0 0;
}
</style>
