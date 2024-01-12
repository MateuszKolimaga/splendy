import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "./pages/LoginPage.vue";
import HomePage from "./pages/HomePage.vue";
import MainDashboardPage from "./pages/dashboard/MainDashboardPage.vue";
import DashboardSplitPage from "./pages/split/DashboardSplitPage.vue";
import SocialSplitPage from "./pages/split/SocialSplitPage.vue";
import SignUpPage from "./pages/SignUpPage.vue";
import SignUpDetailPageVue from "./pages/SignUpDetailPage.vue";
import { loginTrigger } from "./composables/routerTriggers";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
    beforeEnter: loginTrigger,
  },
  {
    path: "/sign-up",
    name: "SignUp",
    component: SignUpPage,
  },
  {
    path: "/sign-up-detail",
    name: "SignUpDetail",
    component: SignUpDetailPageVue,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: MainDashboardPage,
  },
  {
    path: "/split",
    name: "Split",
    component: DashboardSplitPage
  },
  {
    path: "/split-social",
    name: "SplitSocial",
    component: SocialSplitPage
  },
  { 
    path: '/split-dashboard/:teamId',
    name: 'SplitDashboard',
    component: DashboardSplitPage, 
    props: true 
  }
];

const router = createRouter({
  history: createWebHistory(),
  //@ts-ignore
  routes,
});

export default router;
