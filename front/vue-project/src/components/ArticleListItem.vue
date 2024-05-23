<template>
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
</style>
