<template>
    <div>
      <h3>게시글 목록</h3>
      <ArticleListItem 
        v-for="article in store.articles"
        :key="article.id"
        :article="article"
      />
    </div>
  </template>
  
  <script setup>
  import { useCounterStore } from '@/stores/counter'
  import ArticleListItem from '@/components/ArticleListItem.vue'
  
  const store = useCounterStore()
  


  </script>
  

      <!-- <table class="article-table">
        <thead>
          <tr>
            <th class="narrow">번호</th>
            <th>닉네임</th>
            <th>게시글 제목</th>
            <th>댓글 수</th>
            <th>등록 날짜</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(article, index) in articles" :key="article.id">
            <td class="narrow">{{ index + 1 }}</td>
            <td>{{ article.user }}</td>
            <td>{{ article.title }}</td>
            <td>{{ article.comments ? article.comments.length : 0 }}</td>
            <td>{{ new Date(article.created_at).toLocaleDateString() }}</td>
          </tr>
        </tbody>
      </table> -->