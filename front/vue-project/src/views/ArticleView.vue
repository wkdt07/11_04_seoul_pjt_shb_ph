<!-- <template>
  <div class="article-page">
    <header>
      <h1>유저 게시판</h1>
      <RouterLink class="create-link" :to="{ name: 'CreateView' }">
        글 쓰기
      </RouterLink>
    </header>
    <ArticleList />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'

const store = useCounterStore()

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.article-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  background-color: #fff;
  font-size: 16px;
  color: #333;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  padding: 20px;
  box-sizing: border-box;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
}

h1 {
  font-size: 35px;
}

.create-link {
  border-radius: 3px;
  background-color: #2db2ff;
  color: white;
  width: 120px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  box-sizing: border-box;
  font-size: 14px;
  text-decoration: none;
  cursor: pointer;
  opacity: 0.8;
}

.create-link:hover {
  opacity: 1;
}
</style> -->


<!--  집 가기 전!!!  -->


<template>
  <div class="article-page">
    <header>
      <h1>유저 게시판</h1>
      <RouterLink class="create-link" :to="{ name: 'CreateView' }">
        글 쓰기
      </RouterLink>
    </header>
    <ArticleList />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'

const store = useCounterStore()

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.article-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  background-color: #fff;
  font-size: 16px;
  color: #333;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  padding: 20px;
  box-sizing: border-box;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
}

h1 {
  font-size: 35px;
}

.create-link {
  border-radius: 3px;
  background-color: #2db2ff;
  color: white;
  width: 120px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  box-sizing: border-box;
  font-size: 14px;
  text-decoration: none;
  cursor: pointer;
  opacity: 0.8;
}

.create-link:hover {
  opacity: 1;
}
</style>