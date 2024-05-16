<template>
  <span v-if="store.comments !== null">
  <div v-for="comment in store.comments">    
    <p>{{ comment.content }}</p>
    <p>{{ comment.user }}</p>   
    <!-- <RouterLink :to="{name:'createComment',params: { article_pk: article.id }}"></RouterLink> -->
  </div></span>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router';

const store = useCounterStore()

</script>

<style scoped>

</style>