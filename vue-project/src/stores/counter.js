import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore(
    "counter",
    () => {
        const articles = ref([]);
        const token = ref(null);
        const API_URL = "http://127.0.0.1:8000.";

        const signUp = function (user) {
            const { username, password1, password2 } = user;

            axios({
                method: "post",
                url: `${API_URL}/accounts/signup/`,
                data: {
                    username,
                    password1,
                    password2,
                },
            })
                .then((response) => {
                    const password = password1;
                    console.log("회원가입 성공!");
                })
                .catch((error) => console.log(error));
        };
        const logIn = function (user) {
            const { username, password } = user;
            axios({
                method: "post",
                url: `${API_URL}/accounts/login/`,
                data: {
                    username,
                    password,
                },
            })
                .then((res) => {
                    token.value = res.data.key;
                })
                .catch((err) => console.log(err));
            1;
        };
        // 꼭 활성화 하기
        return { articles, API_URL, token, logIn };
    },
    { persist: true }
);
