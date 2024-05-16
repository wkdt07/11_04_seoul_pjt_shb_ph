<template>
    <div>
        <h1>Sign Up Page</h1>
        <form @submit.prevent="signUp">
            <label for="username">username : </label>
            <input type="text" id="username" v-model.trim="username"><br>

            <label for="password1">pw: </label>
            <input type="password" id="password1" v-model.trim="password1"><br>

            <label for="password2"> pw confirm : </label>
            <input type="password" id="password2" v-model.trim="password2">

            <input type="submit" value="signUp">
        </form>
    </div>
</template>
  
<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref } from 'vue'
const store = useCounterStore()
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const signUp = function () {
    const user = {
        username: username.value,
        password1: password1.value,
        password2: password2.value,
    }
    store.signUp(user)
}

</script>
  
<style></style>
  