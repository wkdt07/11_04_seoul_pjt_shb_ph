<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div>
        <label for="title">제목 : </label>
        <input type="text" v-model.trim="title" id="title">
      </div>
      <div>
        <label for="content">내용 :akzj </label>
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
import ArticleListItem from '../components/ArticleListItem.vue';

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

// const createArticle = function () {
//   console.log('Creating article with URL:', `${store.DJANGO_URL}/articles/`)
//   axios({
//     method: 'post',
//     url: `${store.DJANGO_URL}/articles/`,
//     data: {
//       title: title.value,
//       content: content.value
//     },  
//     headers:{
//         Authorization:`Token ${store.token}`
//     }
//   })
//     .then((response) => {
//       router.push({ name: 'ArticleView' })
//     })
//     .catch((error) => {
//       console.log(error)
//     })
// }

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
  
</style>
