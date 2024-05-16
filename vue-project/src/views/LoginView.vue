<template>
    <div>
        <h1>Login Page</h1>
        <form @submit="logIn">
            <label for="id">id: </label>
            <input type="text" id="id" v-model.trim="id">
            <label for="password">pw: </label>
            <input type="password" id="password" v-model.trim="password">


            <input type="submit" value="로그인">
        </form>
    </div>
</template>

<script setup>
import { useCounterStore } from '../stores/counter';
const store = useCounterStore()
import { ref } from 'vue';

const id = ref(null)
const password = ref(null)

const logIn = function () {
    const user = {
        id: id.value,
        pw: password.value
    }
    store.logIn(user)
}
</script>

<style scoped></style>