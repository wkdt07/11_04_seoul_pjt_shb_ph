import { ref, computed, useTransitionState } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token=ref(null)
  const route = useRouter()
  const comments = ref([])

  const getComments = function(){
    axios({
        method:'get',
        url: `${API_URL}/articles/comments/`,
        headers:{
            Authorization:`Token ${token.value}`
          }
    }).then(res=>{comments.value=response.data})
    .catch(err=>console.log(err))
  }

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/articles/`,
      headers:{
        Authorization:`Token ${token.value}`
      }
    })
      .then(response => {
        articles.value = response.data
        
      })
      .catch(error => {
        console.log(error)
      })
  }
  

  const isLogin = computed(()=>{
    if (token.value===null){
      return false
    }
    else{
      return true
    }
  })
  const logIn = function(payload){
    const {username,password}=payload
    axios({
      method:'post',
      url:`${API_URL}/accounts/login/`,
      data:{
        username,password
      }
    }).then(res=>{
      console.log('로그인이 완료되었습니다.')
      console.log(res.data) // 이 안에 토큰 데이터가 존재한다. 
      token.value=res.data.key
      route.push({name:'ArticleView'})
    }).catch(err=>console.log(err))
  }
  const signUp=function(payload){
    const username = payload.username
    const password1=payload.password1
    const password2=payload.password2
    // const {username,password1,password2}=payload
    axios({
      method:'post',
      url: `${API_URL}/accounts/signup/`,
      data:{
        username,password1,password2
      }
    }).then(res=>{
      console.log('회원가입이 완료되었습니다.')
      const password = password1
      logIn({username,password})
    }).catch(err=>console.log(err))

  }
  const logOut = function(){
    token.value = null
    axios({
      method : 'post',
      url:`${API_URL}/accounts/logout/`
    })
  }

  const createComment=function(payload){
    const content = payload.content
    const article_pk=payload.article_pk
    axios({
        method:'post',
        url:`${API_URL}/articles/${article_pk}/comments/`,
        data:{content}
    }).then(res=>console.log('생성완료'))
    .catch(err=>console.log(err))
  }
  return { articles, API_URL, getArticles,signUp,logIn,token,isLogin,logOut,getComments }
}, { persist: true })
