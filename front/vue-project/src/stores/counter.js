// // // import { ref, computed, useTransitionState } from 'vue'
// // // import { defineStore } from 'pinia'
// // // import axios from 'axios'
// // // import { useRouter } from 'vue-router'
// // // export const useCounterStore = defineStore('counter', () => {
// // //   const articles = ref([])
// // //   const DJANGO_URL = 'http://127.0.0.1:8000'
// // //   const token=ref(null)
// // //   const route = useRouter()
// // //   const comments = ref([])

// // //   const getComments = function(){
// // //     axios({
// // //         method:'get',
// // //         url: `${DJANGO_URL}/articles/comments/`,
// // //         headers:{
// // //             Authorization:`Token ${token.value}`
// // //           }
// // //     }).then(res=>{comments.value=response.data})
// // //     .catch(err=>console.log(err))
// // //   }

// // //   const getArticles = function () {
// // //     axios({
// // //       method: 'get',
// // //       url: `${DJANGO_URL}/articles/`,
// // //       headers:{
// // //         Authorization:`Token ${token.value}`
// // //       }
// // //     })
// // //       .then(response => {
// // //         articles.value = response.data
        
// // //       })
// // //       .catch(error => {
// // //         console.log(error)
// // //       })
// // //   }
  

// // //   const isLogin = computed(()=>{
// // //     if (token.value===null){
// // //       return false
// // //     }
// // //     else{
// // //       return true
// // //     }
// // //   })
// // //   const logIn = function(payload){
// // //     const {username,password}=payload
// // //     console.log(payload)
// // //     console.log(username)
// // //     console.log(password)
    
// // //     axios({
// // //       method:'post',
// // //       url:`${DJANGO_URL}/accounts/login/`,
// // //       data:{
// // //         username,password
// // //       }
// // //     }).then(res=>{
// // //       console.log('로그인이 완료되었습니다.')
// // //       console.log(res.data) // 이 안에 토큰 데이터가 존재한다. 
// // //       token.value=res.data.key
// // //       route.push({name:'ArticleView'})
// // //     }).catch((err)=>{
// // //       alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.')
// // //       console.log(err)
// // //     })
// // //   }
// // //   const signUp=function(payload){
// // //     // const username = payload.username
// // //     // const password1=payload.password1
// // //     // const password2=payload.password2
// // //     const {username,
// // //       password1,
// // //       password2,
// // //       email,
// // //       name,
// // //       age,
// // //       now_money,
// // //       money_per_year,
// // //       fav_place}=payload
// // //     axios({
// // //       method:'post',
// // //       url: `${DJANGO_URL}/accounts/registration/`,
// // //       data:{
// // //         username,
// // //         password1,
// // //         password2,
// // //         email,
// // //         name,
// // //         age,
// // //         now_money,
// // //         money_per_year,
// // //         fav_place,
// // //       }
// // //     }).then(res=>{
// // //       console.log('회원가입이 완료되었습니다.')
// // //       const password = password1
// // //       logIn({username,password})
// // //     }).catch((err)=>{
// // //       alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.')
// // //       console.log(DJANGO_URL)
// // //       console.log('Error response=',err.response)

// // //     })
// // //   }
// // //   const logOut = function(){
// // //     token.value = null
// // //     axios({
// // //       method : 'post',
// // //       url:`${DJANGO_URL}/accounts/logout/`
// // //     })
// // //   }

// // //   const createComment=function(payload){
// // //     const content = payload.content
// // //     const article_pk=payload.article_pk
// // //     axios({
// // //         method:'post',
// // //         url:`${DJANGO_URL}/articles/${article_pk}/comments/`,
// // //         data:{content}
// // //     }).then(res=>console.log('생성완료'))
// // //     .catch(err=>console.log(err))
// // //   }
// // //   return { articles, DJANGO_URL, getArticles,signUp,logIn,token,isLogin,logOut,getComments }
// // // }, { persist: true })
// // import { ref, computed } from 'vue'
// // import { defineStore } from 'pinia'
// // import axios from 'axios'
// // import { useRouter } from 'vue-router'

// // export const useCounterStore = defineStore('counter', () => {
// //   const articles = ref([])
// //   const DJANGO_URL = 'http://127.0.0.1:8000'
// //   const token = ref(null)
// //   const router = useRouter()
// //   const comments = ref([])

// //   const getComments = function(article_pk) {
// //     axios({
// //       method: 'get',
// //       url: `${DJANGO_URL}/articles/${article_pk}/comments/`,
// //       headers: {
// //         Authorization: `Token ${token.value}`
// //       }
// //     }).then(response => {
// //       comments.value = response.data
// //     }).catch(err => console.log(err))
// //   }

// //   const getArticles = function() {
// //     axios({
// //       method: 'get',
// //       url: `${DJANGO_URL}/articles/`,
// //       headers: {
// //         Authorization: `Token ${token.value}`
// //       }
// //     }).then(response => {
// //       articles.value = response.data
// //     }).catch(error => {
// //       console.log(error)
// //     })
// //   }

// //   const isLogin = computed(() => {
// //     return token.value !== null
// //   })

// //   const logIn = function(payload) {
// //     const { username, password } = payload
// //     axios({
// //       method: 'post',
// //       url: `${DJANGO_URL}/accounts/login/`,
// //       data: {
// //         username,
// //         password
// //       }
// //     }).then(res => {
// //       console.log('로그인이 완료되었습니다.')
// //       token.value = res.data.key
// //       router.push({ name: 'ArticleView' })
// //     }).catch(err => {
// //       alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.')
// //       console.log(err)
// //     })
// //   }

// //   const signUp = function(payload) {
// //     const {
// //       username,
// //       password1,
// //       password2,
// //       email,
// //       name,
// //       age,
// //       now_money,
// //       money_per_year,
// //       fav_place
// //     } = payload
// //     axios({
// //       method: 'post',
// //       url: `${DJANGO_URL}/accounts/registration/`,
// //       data: {
// //         username,
// //         password1,
// //         password2,
// //         email,
// //         name,
// //         age,
// //         now_money,
// //         money_per_year,
// //         fav_place
// //       }
// //     }).then(res => {
// //       console.log('회원가입이 완료되었습니다.')
// //       const password = password1
// //       logIn({ username, password })
// //     }).catch(err => {
// //       alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.')
// //       console.log(err)
// //     })
// //   }

// //   const logOut = function() {
// //     token.value = null
// //     axios({
// //       method: 'post',
// //       url: `${DJANGO_URL}/accounts/logout/`
// //     })
// //   }

// //   const createComment = function(payload) {
// //     const { content, article_pk} = payload
// //     axios({
// //       method: 'post',
// //       url: `${DJANGO_URL}/articles/${article_pk}/comments/`,
// //       data: { content }
// //     }).then(res => console.log('생성완료'))
// //     .catch(err => console.log(err))
// //   }

// //   return { 
// //     articles, 
// //     DJANGO_URL, 
// //     getArticles, 
// //     signUp, 
// //     logIn, 
// //     token, 
// //     isLogin, 
// //     logOut, 
// //     getComments, 
// //     createComment 
// //   }
// // }, { persist: true })
// import { ref, computed } from 'vue';
// import { defineStore } from 'pinia';
// import axios from 'axios';

// const DJANGO_URL = 'http://127.0.0.1:8000';

// export const useCounterStore = defineStore('counter', () => {
//   const articles = ref([]);
//   const token = ref(null);
//   const comments = ref([]);

//   const getComments = async (article_pk) => {
//     try {
//       const response = await axios.get(`${DJANGO_URL}/articles/${article_pk}/comments/`, {
//         headers: {
//           Authorization: `Token ${token.value}`
//         }
//       });
//       comments.value = response.data;
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   const getArticles = async () => {
//     try {
//       const response = await axios.get(`${DJANGO_URL}/articles/`, {
//         headers: {
//           Authorization: `Token ${token.value}`
//         }
//       });
//       articles.value = response.data;
//     } catch (error) {
//       console.log(error);
//     }
//   };

//   const isLogin = computed(() => {
//     return token.value !== null;
//   });

//   const logIn = async (payload) => {
//     const { username, password } = payload;
//     try {
//       const res = await axios.post(`${DJANGO_URL}/accounts/login/`, { username, password });
//       console.log('로그인이 완료되었습니다.');
//       token.value = res.data.key;
//       // router.push({ name: 'ArticleView' }); // 라우터는 컴포넌트에서 사용
//     } catch (err) {
//       alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.');
//       console.log(err);
//     }
//   };

//   const signUp = async (payload) => {
//     const {
//       username,
//       password1,
//       password2,
//       email,
//       name,
//       age,
//       now_money,
//       money_per_year,
//       fav_place
//     } = payload;
//     try {
//       await axios.post(`${DJANGO_URL}/accounts/registration/`, {
//         username,
//         password1,
//         password2,
//         email,
//         name,
//         age,
//         now_money,
//         money_per_year,
//         fav_place
//       });
//       console.log('회원가입이 완료되었습니다.');
//       const password = password1;
//       await logIn({ username, password });
//     } catch (err) {
//       alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.');
//       console.log(err);
//     }
//   };

//   const logOut = async () => {
//     token.value = null;
//     try {
//       await axios.post(`${DJANGO_URL}/accounts/logout/`);
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   const createComment = async (payload) => {
//     const { content, article_pk } = payload;
//     try {
//       await axios.post(`${DJANGO_URL}/articles/${article_pk}/comments/`, { content }, {
//         headers: {
//           Authorization: `Token ${token.value}`
//         }
//       });
//       console.log('댓글 생성 완료');
//       await getComments(article_pk); // 댓글 생성 후 댓글 목록 갱신
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   return { 
//     articles, 
//     getArticles, 
//     signUp, 
//     logIn, 
//     token, 
//     isLogin, 
//     logOut, 
//     comments,
//     getComments, 
//     createComment 
//   };
// }, { persist: true });


// // 이전에 통합하기 전에 성공한 코드
// import { ref, computed } from 'vue';
// import { defineStore } from 'pinia';
// import axios from 'axios';

// const DJANGO_URL = 'http://127.0.0.1:8000';

// export const useCounterStore = defineStore('counter', () => {
//   const articles = ref([]);
//   const token = ref(null);
//   const comments = ref([]);

//   const getComments = async (article_pk) => {
//     try {
//       const response = await axios.get(`${DJANGO_URL}/articles/${article_pk}/comments/`, {
//         headers: {
//           Authorization: `Token ${token.value}`
//         }
//       });
//       comments.value = response.data;
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   const getArticles = async () => {
//     try {
//       const response = await axios.get(`${DJANGO_URL}/articles/`, {
//         headers: {
//           Authorization: `Token ${token.value}`
//         }
//       });
//       articles.value = response.data;
//     } catch (error) {
//       console.log(error);
//     }
//   };

//   const getArticle = async (article_pk) => {
//     try {
//       const response = await axios.get(`${DJANGO_URL}/articles/${article_pk}/`, {
//         headers: {
//           Authorization: `Token ${token.value}`
//         }
//       });
//       return response.data;
//     } catch (error) {
//       console.log(error);
//     }
//   };

//   const isLogin = computed(() => {
//     return token.value !== null;
//   });

//   const logIn = async (payload) => {
//     const { username, password } = payload;
//     try {
//       const res = await axios.post(`${DJANGO_URL}/accounts/login/`, { username, password });
//       console.log('로그인이 완료되었습니다.');
//       token.value = res.data.key;
//     } catch (err) {
//       alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.');
//       console.log(err);
//     }
//   };

//   const signUp = async (payload) => {
//     const {
//       username,
//       password1,
//       password2,
//       email,
//       name,
//       age,
//       now_money,
//       money_per_year,
//       fav_place
//     } = payload;
//     try {
//       await axios.post(`${DJANGO_URL}/accounts/registration/`, {
//         username,
//         password1,
//         password2,
//         email,
//         name,
//         age,
//         now_money,
//         money_per_year,
//         fav_place
//       });
//       console.log('회원가입이 완료되었습니다.');
//       const password = password1;
//       await logIn({ username, password });
//     } catch (err) {
//       alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.');
//       console.log(err);
//     }
//   };

//   const logOut = async () => {
//     token.value = null;
//     try {
//       await axios.post(`${DJANGO_URL}/accounts/logout/`);
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   const createComment = async (payload) => {
//     const { content, article_pk } = payload;
//     try {
//       await axios.post(`${DJANGO_URL}/articles/${article_pk}/comments/`, { content }, {
//         headers: {
//           Authorization: `Token ${token.value}`
//         }
//       });
//       console.log('댓글 생성 완료');
//       await getComments(article_pk); // 댓글 생성 후 댓글 목록 갱신
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   return { 
//     articles, 
//     getArticles, 
//     getArticle,
//     signUp, 
//     logIn, 
//     token, 
//     isLogin, 
//     logOut, 
//     comments,
//     getComments, 
//     createComment 
//   };
// }, { persist: true });
import { ref, computed, watch } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

const DJANGO_URL = 'http://127.0.0.1:8000';

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([]);
  const token = ref(null);
  const comments = ref([]);
  const router = useRouter();

  // 사용자 정보 관련 상태 변수
  const userInfo = ref();
  const userContractDeposits = ref();
  const userContractSavings = ref();

  // 사용자 정보 변경 감지
  watch(userInfo, () => {
    userContractDeposits.value = userInfo.value?.contract_deposit;
    userContractSavings.value = userInfo.value?.contract_saving;
  });

  // 사용자 정보를 가져오는 함수
  const getUserInfo = async (username) => {
    try {
      const response = await axios.get(`${DJANGO_URL}/users/${username}/info/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      userInfo.value = response.data;
    } catch (err) {
      console.log(err);
    }
  };

  const getComments = async (article_pk) => {
    try {
      const response = await axios.get(`${DJANGO_URL}/articles/${article_pk}/comments/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      comments.value = response.data;
    } catch (err) {
      console.log(err);
    }
  };

  const getArticles = async () => {
    try {
      const response = await axios.get(`${DJANGO_URL}/articles/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      articles.value = response.data;
    } catch (error) {
      console.log(error);
    }
  };

  const getArticle = async (article_pk) => {
    try {
      const response = await axios.get(`${DJANGO_URL}/articles/${article_pk}/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      return response.data;
    } catch (error) {
      console.log(error);
    }
  };

  const isLogin = computed(() => {
    return token.value !== null;
  });

  const logIn = async (payload) => {
    const { username, password } = payload;
    try {
      const res = await axios.post(`${DJANGO_URL}/accounts/login/`, { username, password });
      console.log('로그인이 완료되었습니다.');
      token.value = res.data.key;
      await getUserInfo(username);
      router.push({ name: 'ArticleView' });
    } catch (err) {
      alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.');
      console.log(err);
    }
  };

  const signUp = async (payload) => {
    const {
      username,
      password1,
      password2,
      email,
      name,
      age,
      now_money,
      money_per_year,
      fav_place
    } = payload;
    try {
      await axios.post(`${DJANGO_URL}/accounts/registration/`, {
        username,
        password1,
        password2,
        email,
        name,
        age,
        now_money,
        money_per_year,
        fav_place
      });
      console.log('회원가입이 완료되었습니다.');
      const password = password1;
      await logIn({ username, password });
    } catch (err) {
      alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.');
      console.log(err);
    }
  };

  const logOut = async () => {
    token.value = null;
    try {
      await axios.post(`${DJANGO_URL}/accounts/logout/`);
      token.value = null;
      userInfo.value = [];
      router.push({ name: 'home' });
    } catch (err) {
      console.log(err);
    }
  };

  const createComment = async (payload) => {
    const { content, article_pk } = payload;
    try {
      await axios.post(`${DJANGO_URL}/articles/${article_pk}/comments/`, { content }, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      console.log('댓글 생성 완료');
      await getComments(article_pk); // 댓글 생성 후 댓글 목록 갱신
    } catch (err) {
      console.log(err);
    }
  };

  return { 
    articles, 
    getArticles, 
    getArticle,
    signUp, 
    logIn, 
    token, 
    isLogin, 
    logOut, 
    comments,
    getComments, 
    createComment,
    // 추가된 부분
    userInfo,
    userContractDeposits,
    userContractSavings,
    getUserInfo
  };
}, { persist: true });
