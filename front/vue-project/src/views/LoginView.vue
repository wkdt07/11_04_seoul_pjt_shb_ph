<template>
  <div>
    <form @submit.prevent="logIn">
      <label for="username">username : </label>
      <input
        type="text"
        id="username"
        value="이거 같은데"
        v-model.trim="username"
      /><br />
      <label for="password1">password : </label>
      <input type="password" id="password" v-model.trim="password" /><br />

      <input type="submit" value="logIn" />
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore();
const username = ref(null);
const password = ref(null);

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};
</script>

<style></style>
