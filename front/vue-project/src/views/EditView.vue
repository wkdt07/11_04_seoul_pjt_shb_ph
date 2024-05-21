<template>
  <div>
    <h1>게시글 수정</h1>
    <form @submit.prevent="updateArticle">
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
      <input type="submit" value="수정하기">
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()
const title = ref('')
const content = ref('')
const image = ref(null)  

console.log(route.params)
const fetchArticle = async () => {
  const articleId = route.params.article_pk
  try {
    const response = await axios.get(`${store.DJANGO_URL}/articles/${articleId}/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    title.value = response.data.title
    content.value = response.data.content
  } catch (error) {
    console.log(error)
  }
}

const onFileChange = (e) => {  
  image.value = e.target.files[0]
}

const updateArticle = async () => {
  const articleId = route.params.article_pk
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (image.value) {  
    formData.append('image', image.value)  
  }

  try {
    await axios.put(`${store.DJANGO_URL}/articles/${articleId}/`, formData, {
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

onMounted(fetchArticle)
</script>

<style scoped>

</style>
