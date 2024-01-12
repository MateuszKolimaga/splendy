<template lang="pug">
#app
  main-header-component(v-if="shouldRenderHeader")
  toast-emitter
  router-view
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import router from "./router";
import ToastEmitter from '@/components/ui/ToastEmitter.vue'
import MainHeaderComponent from "./components/headers/MainHeaderComponent.vue";
import { RouteRecordName } from "vue-router";
import { useSignStore } from "./stores/signStore";
import { useTeamStore } from "./stores/teamStore";
import { useToasts } from "./composables/useToasts";

export default defineComponent({
  name: "App",
  components: {
    MainHeaderComponent, ToastEmitter
  },
  setup() {
    const shouldRenderHeader = ref(true);
    const routesWithoutHeader: (RouteRecordName | null | undefined)[] = ["Login", "SignUp", "SignUpDetail"]
    const safeRoutes = [...routesWithoutHeader, "Home"]
    const signStore = useSignStore()
    const { addToast } = useToasts()
    router.beforeEach((to, _, next) => {
      var nextRoute = undefined
      const isRouteUnsafe = safeRoutes.indexOf(to.name) === -1 || to.name == undefined
      const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
      if (signStore.loggedIn) {
        if (!isRouteUnsafe) nextRoute = "Dashboard"
      } else {
        if (isRouteUnsafe) {
          nextRoute="/"
        }
      }

      if (isRouteUnsafe && isMobile) {
        addToast({
          message: 'This app is not suitable for mobile devices. Please use a desktop browser.',
          type: 'warning'
        })
      }

      if (to.query.invitation) {
        const teamStore = useTeamStore()
        teamStore.handleInvitation(to.query.invitation as string)
      }

      shouldRenderHeader.value = routesWithoutHeader.indexOf(nextRoute ?? to.name) === -1
      nextRoute ? next(nextRoute) : next();
    });

    return {
      router,
      shouldRenderHeader,
    };
  }
});
</script>

<style lang="scss">
@import "@/styles/styles.scss";
@import url('https://fonts.cdnfonts.com/css/lato');

html,
body {
  height: 100%;
  margin: 0;
  width: auto!important; 
  overflow-x: hidden!important;
}

#app {
  display: flex;
  flex-flow: column;
  font-family: Ubuntu, Lato;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.fixed-h {
  height: calc(100vh - $header-h);
}
</style>
