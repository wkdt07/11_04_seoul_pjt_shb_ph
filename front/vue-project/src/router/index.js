import { createRouter, createWebHistory } from 'vue-router'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import CreateCommentView from '@/views/CreateCommentView.vue'
import MapView from '@/views/MapView.vue'
import { useCounterStore } from '@/stores/counter'
import DepositListView from '@/components/DepositListView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'ArticleView',
      component: ArticleView
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
        path:'/articles/:article_pk/createComment',
        name:'createComment',
        component:CreateCommentView
    },
    {
      path:'/map',
      name:'MapView',
      component:MapView
    },
    {
      path:'/depositList',
      name:'DepositListView',
      component:DepositListView
    }
    ,
    {
      path:'/profile/:username',
      name:'ProfileView',
      component:ProfileView
    }

]
})

router.beforeEach((to,from)=>{
  const store=useCounterStore()
  if(to.name==='ArticleView'&& !store.isLogin){
    window.alert('로그인이 필요합니다.')
    console.log(store.isLogin)
    console.log(store.token)
    return {name:'LogInView'}
  }
  if ((to.name === 'SignUpView'||to.name==='LogInView') && (store.isLogin)){
    window.alert('이미 로그인이 되어있습니다')
    return {name:'ArticleView'}
  }

})
export default router
