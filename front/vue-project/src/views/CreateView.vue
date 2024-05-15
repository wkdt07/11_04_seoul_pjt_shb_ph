<template>
    <div>
        <h1>게시글 작성</h1>
        <form>
            <div>
                <label for="title">제목 : </label>
                <input type="text" v-model.trim="title" id="title">
            </div>
            <div>
                <label for="content">내용 :</label>
                <textarea v-model.trim="content" id="content"></textarea>
            </div>
        </form>
        <input type="submit">
    </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router'

const store = useCounterStore()
const title = ref(null)
const content = ref(null)
const router = useRouter()

const createArticle = function () {
    axios({
        method: 'post',
        url: `http://localhost:5173/articles/`,

        // url: `${store.API_URl}/api/v1/articles/`,
        data: {
            title: title.value,
            content: content.value
        },
    }).then((response) => {
        console.log(response.data)
    }).catch((error) => {
        console.log(error)
    })
}
</script>

<style scoped></style>