<!-- <template>
  <div class="article-list-item">
    <RouterLink :to="{ name: 'DetailView', params: { id: article.id }}">
      <table class="article-table">
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
          <tr>
            <td class="narrow">{{ article.id }}</td>
            <td>{{ article.user }}</td>
            <td>{{ article.title }}</td>
            <td>{{ article.comments ? article.comments.length : 0 }}</td>
            <td>{{ new Date(article.created_at).toLocaleDateString() }}</td>
          </tr>
        </tbody>
      </table>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object
})
</script>

<style scoped>
.article-list-item {
  margin-bottom: 10px;
}

.article-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.article-table th,
.article-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.article-table th {
  background-color: #f2f2f2;
}

.article-table .narrow {
  width: 50px;
}
</style> -->


<!-- 이 위가 집 가기 전 수정 전!!!!!!!!! -->

<template>
  <div class="article-list-item">
    <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" class="article-link">
      <div class="article-card">
        <div class="article-header">
          <span class="article-id">#{{ article.id }}</span>
          <span class="article-user">{{ article.user }}</span>
          <span class="article-date">{{ new Date(article.created_at).toLocaleDateString() }}</span>
        </div>
        <div class="article-body">
          <h2 class="article-title">{{ article.title }}</h2>
          <p class="article-comments">댓글 수: {{ article.comments ? article.comments.length : 0 }}</p>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object
})
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.article-list-item {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.article-link {
  text-decoration: none;
  color: inherit;
  width: 100%;
  max-width: 800px;
  /* 카드를 더 넓게 설정 */
}

.article-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  width: 800px;
}

.article-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.article-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.article-id {
  font-weight: bold;
  color: #2db2ff;
}

.article-user {
  font-style: italic;
  color: #666;
}

.article-date {
  color: #999;
}

.article-body {
  display: flex;
  flex-direction: column;
}

.article-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 10px;
  color: #333;
}

.article-comments {
  font-size: 14px;
  color: #888;
}
</style>