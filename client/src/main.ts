import { createApp } from "vue";
import App from "./App.vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import router from "./router";
import { loadIcons } from "./styles/icons/icons";
import { createPinia } from 'pinia'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"
import './styles/custom-bootsrap.scss'
// import { VueRecaptcha } from 'vue-recaptcha'

const pinia = createPinia()
pinia.use(piniaPluginPersistedState)
loadIcons()
createApp(App)
  .use(router)
  .use(pinia)
  .component("font-awesome-icon", FontAwesomeIcon)
  .mount("#app");
