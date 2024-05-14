<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'ArticlesView' }">Articles</RouterLink>
      <RouterLink :to="{ name: 'SignUpView' }">Sign Up Page</RouterLink>
      <RouterLink :to="{ name: 'LoginView' }">Login Page</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<style scoped></style>