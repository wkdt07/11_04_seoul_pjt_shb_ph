import { createRouter, createWebHistory } from "vue-router";
import ArticleView from "@/views/ArticleView.vue";

import { useCounterStore } from "@/stores/counter";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "ArticlesView",
            component: ArticleView,
        },
    ],
});

export default router;
