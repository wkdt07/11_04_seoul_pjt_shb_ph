<template>
  <div>
    <!-- <span>{{ article.id }}</span> -->
    <RouterLink 
      :to="{ name: 'DetailView', params: { id: article.id }}"
      >    <p>{{ article.title }}</p>
    </RouterLink>
   
    <!-- {{ article }} -->
    </div>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router'

  defineProps({
    article: Object
  })
  </script>
  