import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
    const articles = ref([]);
    // const API_URL = "http://127.0.0.1:8000.";
    // 꼭 활성화 하기
    return { articles, API_URL }, { persist: true };
});
