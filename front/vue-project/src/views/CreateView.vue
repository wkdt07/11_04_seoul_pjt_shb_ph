<!-- <template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div>
        <label for="title">제목 : </label>
        <input type="text" v-model.trim="title" id="title">
      </div>
      <div>
        <label for="content">내용 : </label>
        <textarea v-model.trim="content" id="content"></textarea>
      </div>
      <div>
        <label for="image">이미지 : </label>
        <input type="file" @change="onFileChange" id="image">
      </div>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import ArticleListItem from '@/components/ArticleListItem.vue';

const store = useCounterStore()
const title = ref(null)
const content = ref(null)
const image = ref(null)
const router = useRouter()

// URL 디버깅을 위한 로그 추가
console.log('DJANGO_URL:', store.DJANGO_URL)
console.log('store:', store)

const onFileChange = (e) => {  
  image.value = e.target.files[0]
}

const createArticle = async () => {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (image.value) {
    formData.append('image', image.value)
  }

  try {
    await axios.post(`${store.DJANGO_URL}/articles/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Token ${store.token}`
      }
    })
    router.push({ name: 'ArticleView' })
  } catch (error) {
    console.log(error)
  }
}
</script>

<style>
  
</style> -->


<template>
  <div class="create-article-page">
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle" class="article-form">
      <div class="form-group">
        <label for="title">제목 : </label>
        <input type="text" v-model.trim="title" id="title" class="form-control">
      </div>
      <div class="form-group">
        <label for="content">내용 : </label>
        <textarea v-model.trim="content" id="content" class="form-control"></textarea>
      </div>
      <div class="form-group">
        <label for="image">이미지 : </label>
        <input type="file" @change="onFileChange" id="image" class="form-control">
      </div>
      <input type="submit" value="작성" class="submit-button">
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const title = ref(null)
const content = ref(null)
const image = ref(null)
const router = useRouter()

const onFileChange = (e) => {
  image.value = e.target.files[0]
}

const createArticle = async () => {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (image.value) {
    formData.append('image', image.value)
  }

  try {
    await axios.post(`${store.DJANGO_URL}/articles/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Token ${store.token}`
      }
    })
    router.push({ name: 'ArticleView' })
  } catch (error) {
    console.log(error)
  }
}
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.create-article-page {
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

h1 {
  font-size: 35px;
  margin-bottom: 20px;
}

.article-form {
  width: 100%;
  max-width: 600px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  box-sizing: border-box;
}

.submit-button {
  background-color: #2db2ff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  border-radius: 4px;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0a73d9;
}
</style>