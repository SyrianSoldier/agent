import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/chat",
    name: "home",
    component: () =>  import(/* webpackChunkName: "chat" */ "@/components/Chat/index.vue")
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router
