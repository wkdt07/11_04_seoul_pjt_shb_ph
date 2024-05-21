import { createRouter, createWebHistory } from 'vue-router'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import CreateCommentView from '@/views/CreateCommentView.vue'
import MapView from '@/views/MapView.vue'
import { useCounterStore } from '@/stores/counter'
import DepositListView from '@/components/DepositListView.vue'
import ProfileView from '../views/ProfileView.vue'
import ProductDetailView from "@/components/ProductDetailView.vue"
import ExchangeView from '@/views/Exchangeview.vue'
import MainPage from '@/components/MainPage.vue'
import EditView from '@/views/EditView.vue'
import ProfileEditView from '@/views/ProfileEditView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/article',
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
      name: 'LoginView',
      component: LoginView
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
    },
    {
      path:'/profile/:username',
      name:'ProfileView',
      component:ProfileView
    },
    {
      path: '/profile/:username/edit',
      name: 'ProfileEditView',
      component: ProfileEditView
    },
    {
      path:'/exchange',
      name:'ExchangeView',
      component:ExchangeView
    },
    {
      path:'/productDetail/:fin_prdt_cd',
      name:'ProductDetailView',
      component:ProductDetailView
    },
    {
      path:'/',
      name:'home',
      component:MainPage
    },
    {
      path: '/edit/:article_pk',
      name: 'EditView',
      component: EditView
    },

]
})
router.beforeEach((to,from)=>{
  const store=useCounterStore()
  if(to.name==='ArticleView'&& !store.isLogin){
    window.alert('로그인이 필요합니다.')
    console.log(store.isLogin)
    console.log(store.token)
    return {name:'LoginView'}
  }
  if ((to.name === 'SignUpView'||to.name==='LoginView') && (store.isLogin)){
    window.alert('이미 로그인이 되어있습니다')
    return {name:'home'}
  }
  if ((to.name ==='LogOutView')&& !store.isLogin){
    window.alert('아직 로그인하지 않았습니다.')
    return {name:'LoginView'}
  }
})
export default router
