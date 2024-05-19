<template>
    <div>
      <h5>{{ article.id }}</h5>
      <p>{{ article.title }}</p>
      <p>{{ article.content }}</p>
      <RouterLink 
        :to="{ name: 'DetailView', params: { id: article.id }}"
      >
      [DETAIL]
    </RouterLink>
    {{ article }}
    <!-- 조회용
      <CommentList
      :article_pk="article.id"
      /> -->
      <!-- <RouterLink :to="{name:'createComment',params: { article_pk: article.id }}"></RouterLink>
   -->
    </div>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router'
  // import CommentList from './CommentList.vue';
  // import { RouterLink } from 'vue-router';
  
  defineProps({
    article: Object
  })
  </script>
  