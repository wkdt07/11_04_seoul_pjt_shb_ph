import { createRouter, createWebHistory } from "vue-router";
import ArticleView from "@/views/ArticleView.vue";

import { useCounterStore } from "@/stores/counter";
const router = createRouter({
    routes: [
        {
            path: "/",
            name: "ArticlesView",
            component: ArticleView,
        },
        {
            path: "/login",
            name: "LoginView",
            component: LoginView,
        },
        {
            path: "/signup",
            name: "signUpView",
            component: SignUpView,
        },
    ],
});

export default router;
