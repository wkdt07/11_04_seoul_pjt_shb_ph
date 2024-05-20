<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '../stores/counter'
import BarChartDetail from '@/components/BarChartDetailView.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월', align: 'end', width: '12%', key: '6month' },
  { title: '12개월', align: 'end', width: '12%', key: '12month' },
  { title: '24개월', align: 'end', width: '12%', key: '24month' },
  { title: '36개월', align: 'end', width: '12%', key: '36month' },
]

const deposits = ref([])
const depositLength = computed(() => deposits.value.length)

const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedDepositSimple = ref(null)
const selectedDeposit = ref(null)
const selectedDepositCode = computed(() => selectedDepositSimple.value?.['deposit_code'])
const dialog = ref(false)
const loading = ref(false)
const sortKey = ref('')
const sortOrder = ref(1) // 1: ascending, -1: descending

const averageIntrRate = [3.45, 4.08, 3.4, 3.35]
const intrRate = ref([null, null, null, null])
const intrRate2 = ref([null, null, null, null])



const isContractDeposit = computed(() => {
  const userInfo = useCounterStore().userInfo;
  
  // userInfo가 정의되어 있는지 확인
  if (!userInfo) {
    console.error("userInfo is undefined");
    return false;
  }
  
  // userInfo.contract_deposit가 배열인지 확인
  const contractDepositArray = Array.isArray(userInfo.contract_deposit) ? userInfo.contract_deposit : [];
  
  return contractDepositArray.some(e => e['deposit_code'] === selectedDepositCode.value);
});

const store = useCounterStore()
const router = useRouter()

const makeItems = function (item) {
  const result = {
    'deposit_code': item['fin_prdt_cd'],
    'dcls_month': item['dcls_month'],
    'kor_co_nm': item['kor_co_nm'],
    'name': item['fin_prdt_nm'],
    '6month': null,
    '12month': null,
    '24month': null,
    '36month': null,
  }

  for (const option of item['options']) {
    const saveTrm = option['save_trm']

    if (saveTrm === "6") {
      result['6month'] = option['intr_rate']
    } else if (saveTrm === "12") {
      result['12month'] = option['intr_rate']
    } else if (saveTrm === "24") {
      result['24month'] = option['intr_rate']
    } else if (saveTrm === "36") {
      result['36month'] = option['intr_rate']
    }
  }

  return result
}

const financialData = ref([])

const make_data = function () {
  axios.get(`${store.DJANGO_URL}/financial/make_financial_data/`)
    .then((res) => {
      financialData.value = res.data || []
      console.log('받아온 데이터=', financialData.value)
    }).catch((err) => {
      console.log('에러가 발생했습니다. error=', err)
    })
}

const getAllDeposit = function () {
  loading.value = true
  axios.get(`${store.DJANGO_URL}/financial/deposit_list/`)
    .then((res) => {
      const results = res.data || []
      deposits.value = []  // 기존 데이터 초기화
      console.log(results)
      for (const item of results) {
        deposits.value.push(makeItems(item))
        if (!banks.value.includes(item['kor_co_nm'])) {
          banks.value.push(item['kor_co_nm'])
        }
      }
      loading.value = false
    })
    .catch((err) => {
      console.log(err)
      loading.value = false
    })
}

const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllDeposit()
  } else {
    loading.value = true
    axios.get(`${store.DJANGO_URL}/financial/get_bank_deposit/${selectedBank.value}/`)
      .then((res) => {
        deposits.value = []
        const results = res.data
        for (const item of results) {
          deposits.value.push(makeItems(item))
        }
        loading.value = false
      })
      .catch((err) => {
        console.log(err)
        loading.value = false
      })
  }
}

const sort = function (key) {
  sortKey.value = key
  sortOrder.value *= -1

  deposits.value.sort((a, b) => {
    if (a[key] < b[key]) return -1 * sortOrder.value
    if (a[key] > b[key]) return 1 * sortOrder.value
    return 0
  })
}

const reset = function () {
  selectedBank.value = '전체 보기'
  getAllDeposit()
}

const close = function () {
  dialog.value = false
}


const getDeposit = async function () {
  if (!selectedDepositCode.value) {
    console.error('selectedDepositCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/`);
    const data = res.data;
    console.log("Deposit data:", data);  // 데이터 확인용 콘솔 로그 추가
    selectedDeposit.value = {
      '가입자 수': data.contract_users,
      '공시 제출월': data['dcls_month'],
      '금융 회사명': data['kor_co_nm'],
      '금융 상품명': data['fin_prdt_nm'],
      '가입 방법': data['join_way'],
      '만기 후 이자율': data['mtrt_int'],
      '우대 조건': data['spcl_cnd'],
      '가입 대상': data['join_member'],
      '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
      '최고 한도': data['max_limit'],
      '기타 유의사항': data['etc_note']
    };
    const optionList = data.options;

    intrRate.value = [null, null, null, null];
    intrRate2.value = [null, null, null, null];

    for (const option of optionList) {
      if (option.save_trm === "6") {
        intrRate.value[0] = option.intr_rate;
        intrRate2.value[0] = option.intr_rate2;
      } else if (option.save_trm === "12") {
        intrRate.value[1] = option.intr_rate;
        intrRate2.value[1] = option.intr_rate2;
      } else if (option.save_trm === "24") {
        intrRate.value[2] = option.intr_rate;
        intrRate2.value[2] = option.intr_rate2;
      } else if (option.save_trm === "36") {
        intrRate.value[3] = option.intr_rate;
        intrRate2.value[3] = option.intr_rate2;
      }
    }

    console.log("intrRate:", intrRate.value);  // 데이터 확인용 콘솔 로그 추가
    console.log("intrRate2:", intrRate2.value);  // 데이터 확인용 콘솔 로그 추가
  } catch (err) {
    console.log(err);
  }
}
const clickRow = async function (data) {
  selectedDepositSimple.value = data;
  intrRate.value = [null, null, null, null];
  intrRate2.value = [null, null, null, null];
  await getDeposit(); // getDeposit이 완료될 때까지 기다림
  dialog.value = true;
}

const addDepositUser = function () {
  axios.post(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/contract/`, null, {
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      store.getUserInfo(store.userInfo.username)
      const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
      if (answer) {
        // router.push({ name: 'productManage', params: { username: store.userInfo.username } })
        router.push({ name: 'ProfileView', params: { username: store.userInfo.username } })

        // 수정 : 임시로 프로필로 이동하게 바꿔놓음
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteDepositUser = function () {
  axios.delete(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/contract/`, {
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      store.getUserInfo(store.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
    })
}

onMounted(async () => {
  await store.getUserInfo(store.userInfo.username);  // userInfo가 로드될 때까지 기다리기
  make_data();
  getAllDeposit();
});

</script>

<template>
  <div>
    <header class="d-flex justify-space-between">
      <h1><span class="color">정기예금</span> 검색하기</h1>
      <div class="w-25">
        <select v-model="selectedBank" @change="clickBank" class="ml-auto bank-select">
          <option v-for="bank in banks" :key="bank">{{ bank }}</option>
        </select>
      </div>
      <button @click="reset">리셋</button>
    </header>
    <hr class="my-3">

    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <h3>{{ selectedDeposit?.['금융 상품명'] }}</h3>
        <div v-if="store.isLogin">
          <button v-if="isContractDeposit" @click.prevent="deleteDepositUser">가입 취소하기</button>
          <button v-else @click.prevent="addDepositUser">가입하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedDeposit" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto">
          <BarChartDetail
            :title="selectedDepositSimple.name"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 예금 금리는 2023년 11월 기준입니다.</p>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>

        <div class="dialog-actions">
          <button @click="close">닫기</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="progress-circular"></div>
    </div>
    <table v-else-if="depositLength !== 0" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in deposits" :key="item.deposit_code" @click="clickRow(item)">
          <td>{{ item['dcls_month'] }}</td>
          <td>{{ item['kor_co_nm'] }}</td>
          <td align="center">{{ item['name'] }}</td>
          <td align="center">{{ item['6month'] }}</td>
          <td align="center">{{ item['12month'] }}</td>
          <td align="center">{{ item['24month'] }}</td>
          <td align="center">{{ item['36month'] }}</td>
        </tr>
      </tbody>
    </table>

    <div v-else class="loading">
      <div class="progress-circular"></div>
    </div>
  </div>
</template>

<style scoped>
.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

.progress-circular {
  width: 80px;
  height: 80px;
  border: 5px solid #1089FF;
  border-radius: 50%;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
}

.dialog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 800px;
  max-width: 90%;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

tbody > tr {
  transition: 200ms;
  cursor: pointer;
}

tbody > tr:hover {
  background-color: rgb(247, 250, 253);
  color: #1089FF;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  background-color: #f2f2f2;
  text-align: left;
}

.bank-select {
  padding: 10px;
  border: 1px solid #1089FF;
  border-radius: 4px;
}
</style>

