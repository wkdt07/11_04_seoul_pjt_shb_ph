import { ref, computed, watch } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';


export const useCounterStore = defineStore('counter', () => {
  const DJANGO_URL = 'http://127.0.0.1:8000';
  const articles = ref([]);
  const token = ref(null);
  const comments = ref([]);
  const router = useRouter();

  // 사용자 정보 관련 상태 변수
  const userInfo = ref(null);
  const userContractDeposits = ref(null);
  const userContractSavings = ref(null);

  // watch(userInfo, () => {
  //   userContractDeposits.value = userInfo.value?.contract_deposit || [];
  //   userContractSavings.value = userInfo.value?.contract_saving || [];
  // });
  const isLogin = computed(() => {
    return token.value !== null && userInfo.value !== null && userInfo.value.username !== undefined;
  });
  
  // 사용자 정보 변경 감지
  watch(userInfo, () => { //특정 값을 찾기 위한 username
    userContractDeposits.value = userInfo.value?.contract_deposit || [];
    userContractSavings.value = userInfo.value?.contract_saving || [];
  });  

  const getUserInfo = async (username) => {
    if(!username) return;
    try {
      const response = await axios.get(`${DJANGO_URL}/users/${username}/info/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      userInfo.value = response.data;
      console.log('getUserInfo의 response=',response.data)
      console.log('getUserInfo 이후의 userInfo.value',userInfo.value)

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
  // 사용자 정보를 가져오는 함수
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
      console.log(response.data)
      return response.data;
    } catch (error) {
      console.log(error);
    }
  };


  const login = async (payload) => {
    const { username, password } = payload;
    console.log(payload)
    try {
      const res = await axios.post(`${DJANGO_URL}/accounts/login/`, { username, password });
      alert(`로그인 되었습니다. ${username}님 환영합니다!`)
      console.log('로그인이 완료되었습니다.');
      token.value = res.data.key;
      console.log(username)
      console.log(password)
      await getUserInfo(username)
      // 로그인 후 사용자 정보 가져오기
      // const userInfoResponse = await axios.get(`${DJANGO_URL}/accounts/${username}/info/`, {
      //   headers: {
      //     Authorization: `Token ${token.value}`
      //   }
      // });
      // userInfo.value = userInfoResponse.data;
      console.log('userInfo=',userInfo.value)
      userContractDeposits.value = userInfo.value.contract_deposit || [];
      userContractSavings.value = userInfo.value.contract_saving || [];
      // console.log('userInfoResponse=',userInfoResponse)
      console.log('userInfo=',userInfo)
      router.push({ name: 'home' });
    } catch (err) {
      alert('잘못된 아이디, 혹은 패스워드입니다.\n다시 시도해주세요.');
      console.log(err);
    }
  };

  // const signUp = async (formData) => {
  //   const {
  //     username,
  //     password1,
  //     password2,
  //     email,
  //     name,
  //     age,
  //     now_money,
  //     money_per_year,
  //     fav_place,
  //     nickname
  //   } = payload;
  //   try {
  //     await axios.post(`${DJANGO_URL}/accounts/registration/`, {
  //       username,
  //       password1,
  //       password2,
  //       email,
  //       name,
  //       age: parseInt(age, 10),  // 문자열을 숫자로 변환
  //       now_money: parseInt(now_money, 10),  // 문자열을 숫자로 변환
  //       money_per_year: parseInt(money_per_year, 10),  // 문자열을 숫자로 변환
  //       fav_place,
  //       nickname
  //     });
  //     alert(`${username}님, 성공적으로 회원가입이 완료되었습니다!`)
  //     console.log('회원가입이 완료되었습니다.');
  //     const password = password1;
  //     await login({ username, password });
  //   } catch (err) {
  //     if (err.response && err.response.data) {
  //       console.log('서버 에러 메시지:', err.response.data);
  //       alert(`회원가입 실패: ${JSON.stringify(err.response.data)}`);
  //     } else {
  //       console.log('회원가입 요청 실패:', err);
  //       alert('회원가입 요청에 실패했습니다. 다시 시도해 주세요.');
  //     }
  //   }
  // };

  const signUp = async (formData) => {
    try {
      const response = await axios.post(`${DJANGO_URL}/accounts/registration/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      alert(`${formData.get('username')}님, 성공적으로 회원가입이 완료되었습니다!`);
      console.log('회원가입이 완료되었습니다.');
      const username = formData.get('username');
      const password = formData.get('password1');
      await login({ username, password });
    } catch (err) {
      if (err.response && err.response.data) {
        console.log('서버 에러 메시지:', err.response.data);
        alert(`회원가입 실패: ${JSON.stringify(err.response.data)}`);
      } else {
        console.log('회원가입 요청 실패:', err);
        alert('회원가입 요청에 실패했습니다. 다시 시도해 주세요.');
      }
    }
  };
  const logOut = async () => {

    try {
      await axios.post(`${DJANGO_URL}/accounts/logout/`);
      token.value = null;
      userInfo.value = null;
      alert('로그아웃 되었습니다.')
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

  // 사용자 정보를 가져오는 함수
  const userArticles = ref([])
  const userComments = ref([])
  const getUserArticles = async (userId) => {
    try {
      const response = await axios.get(`${DJANGO_URL}/users/${userId}/articles/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      console.log('스토어 함수에서 articles data=',response.data)
      console.log('스토어 주소요청주소=',`${DJANGO_URL}/users/${userId}/articles/`)

      userArticles.value = response.data;
    } catch (error) {
      console.log(error);
    }
  };
  const getUserComments = async (userId) => {
    try {
      const response = await axios.get(`${DJANGO_URL}/users/${userId}/comments/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      userComments.value = response.data;
      console.log('comment data=',response.data)
      console.log('요청주소=',`${DJANGO_URL}/users/${userId}/comments/`)
    } catch (error) {
      console.log(error);
    }
  };

  const editComment = async (commentId, content) => {
    try {
      await axios.put(`${DJANGO_URL}/articles/comments/${commentId}/`, { content }, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      console.log('댓글 수정 완료');
    } catch (err) {
      console.log(err);
    }
  };


  const deleteComment = async (commentId) => {
    try {
      await axios.delete(`${DJANGO_URL}/articles/comments/${commentId}/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      console.log('댓글 삭제 완료');
    } catch (err) {
      console.log(err);
    }
  };
  
  // const updateProfile = async (formData) => {
  //   if (!isLogin.value || !userInfo.value) {
  //     console.log('로그인되지 않음 또는 사용자 정보 없음');
  //     return;
  //   }
  
  //   try {
  //     const response = await axios.put(`${DJANGO_URL}/users/profile/`, formData, {
  //       headers: {
  //         Authorization: `Token ${token.value}`,
  //         'Content-Type': 'multipart/form-data'
  //       }
  //     });
  //     userInfo.value = response.data;
  //     console.log('프로필 업데이트 성공:', response.data);
  //   } catch (err) {
  //     console.log('프로필 업데이트 실패:', err);
  //   }
  // };

  const updateProfile = async (formData) => {
    try {
      const response = await axios.put(`${DJANGO_URL}/users/profile/`, formData, {
        headers: {
          Authorization: `Token ${token.value}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      userInfo.value = response.data;
      console.log('프로필 업데이트 성공:', response.data);
    } catch (err) {
      console.log('프로필 업데이트 실패:', err);
      if (err.response && err.response.data) {
        console.log('서버 응답 데이터:', err.response.data);
      }
    }
  };
  const addDepositUser = async (depositCode) => {
    try {
      const response = await axios.post(`${DJANGO_URL}/financial/deposit_list/${depositCode}/contract/`, null, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      await getUserInfo(userInfo.value.username);  // 사용자 정보 갱신
      alert('예금 가입이 완료되었습니다.');
    } catch (err) {
      console.log(err);
      alert('예금 가입에 실패했습니다.');
    }
  };

  const deleteDepositUser = async (depositCode) => {
    try {
      await axios.delete(`${DJANGO_URL}/financial/deposit_list/${depositCode}/contract/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      await getUserInfo(userInfo.value.username);  // 사용자 정보 갱신
      alert('예금 탈퇴가 완료되었습니다.');
    } catch (err) {
      console.log(err);
      alert('예금 탈퇴에 실패했습니다.');
    }
  };

  const addSavingUser = async (savingCode) => {
    try {
      const response = await axios.post(`${DJANGO_URL}/financial/saving_list/${savingCode}/contract/`, null, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      await getUserInfo(userInfo.value.username);  // 사용자 정보 갱신
      alert('적금 가입이 완료되었습니다.');
    } catch (err) {
      console.log(err);
      alert('적금 가입에 실패했습니다.');
    }
  };
  
  const deleteSavingUser = async (savingCode) => {
    try {
      await axios.delete(`${DJANGO_URL}/financial/saving_list/${savingCode}/contract/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      await getUserInfo(userInfo.value.username);  // 사용자 정보 갱신
      alert('적금 탈퇴가 완료되었습니다.');
    } catch (err) {
      console.log(err);
      alert('적금 탈퇴에 실패했습니다.');
    }
  };
  // 제발!!!!!!!!!!!!!!!리턴해!!!!!!!!!!!!!!!!!!!!!!!!!!!
  return { 
    articles, 
    getArticles, 
    getArticle,
    signUp, 
    login, 
    token, 
    isLogin, 
    logOut, 
    comments,
    getComments, 
    createComment,
    userInfo,
    userContractDeposits,
    userContractSavings,
    getUserInfo,
    userArticles,
    userComments,
    getUserArticles,
    getUserComments,
    DJANGO_URL,
    deleteComment,
    editComment,
    updateProfile,
    addDepositUser,
    deleteDepositUser,
    addSavingUser,
    deleteSavingUser,
  };
}, { persist: true });
