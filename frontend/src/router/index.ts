import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router"
import Layout from "@/layout/index.vue"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/chat"
  },

  {
    path: "/chat",
    component: Layout,
    children: [
      {
        path: "",
        name: "chat",
        component: () =>  import(/* webpackChunkName: "chat" */ "@/components/Chat/index.vue")
      }
    ]
  },

  {
    path: "/workspace",
    component: Layout,
    children: [
      {
        path: "",
        name: "workspace",
        component: () => import(/* webpackChunkName: "workspace" */ "@/views/Workspace/index.vue"),
        children: [
          {
            path: "/workspace/modelConfig",
            name: "modelConfig",
            component: () => import(/* webpackChunkName: "modelConfig" */ "@/views/Workspace/components/ModelConfig/index.vue")
          }
        ]
      }
    ]
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
