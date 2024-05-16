<template>
  <div>
    <form @submit.prevent="createComment">
    <label for="content" id="content">댓글:</label>
    <input type="text" id="content" v-model="content">

    <input type="submit" value="작성">
    </form>
  </div>
</template>

<script setup>
import { useCounterStore } from '../stores/counter';
import { useRouter } from 'vue-router'
const store = useCounterStore()
const content=ref('')
router = useRouter()

const createComment=function(){
  const payload = {content : content.value,
  article_pk:router.params.article_pk}
  store.createComment(payload)
}
</script>

<style scoped>

</style>