<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '../stores/counter'
import BarChartDetail from '@/components/BarChartDetailView.vue'
import axios from 'axios'


const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width:'10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width:'32%', key: 'name' },
  { title: '6개월 (Click to sort)', align: 'end', width:'12%', key: '6month' },
  { title: '12개월 (Click to sort)', align: 'end', width:'12%', key: '12month' },
  { title: '24개월 (Click to sort)', align: 'end', width:'12%', key: '24month' },
  { title: '36개월 (Click to sort)', align: 'end', width:'12%', key: '36month' },
]

const deposits = ref([])
const depositLength = computed(() => deposits.value.length)
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedDepositSimple = ref(null)
const selectedDeposit = ref(null)
const selectedDepositCode = computed(() => selectedDepositSimple.value?.['deposit_code'])
const dialog = ref(false)

const averageIntrRate = [3.45, 4.08, 3.4, 3.35]
const intrRate = ref([null, null, null, null])
const intrRate2 = ref([null, null, null, null])


const store = useCounterStore()
const router = useRouter()

const isContractDeposit = computed(() => {
  const userInfo = useCounterStore().userInfo
  return userInfo ? userInfo.contract_deposit.some(e => e['deposit_code'] === selectedDepositCode.value) : false
})

const makeItems = function (item) {
  const result = {
    'deposit_code': item['deposit_code'],
    'dcls_month': item['dcls_month'],
    'kor_co_nm': item['kor_co_nm'],
    'name': item['name'],
    '6month': null,
    '12month': null,
    '24month': null,
    '36month': null,
  }

  if (Array.isArray(item['depositoption_set'])) {
    for (const option of item['depositoption_set']) {
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
  } else {
    console.warn('depositoption_set is not iterable:', item['depositoption_set'])
  }

  return result
}

const getAllDeposit = function () {
  axios.get(`${store.DJANGO_URL}/financial/deposit_list/`)
    .then((res) => {
      // console.log(`${store.DJANGO_URL}/financial/deposit_list/`)
      console.log('response=',res)
      const results = res.data
      console.log('results=',results)
      for (const item of results){
        deposits.value.push(makeItems(item))
        if (!banks.value.includes(item['kor_co_nm'])) {
          banks.value.push(item['kor_co_nm'])
        }
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

onMounted(() => {
  getAllDeposit()
})

const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllDeposit()
  } else {
    axios.get(`${store.DJANGO_URL}/financial/get_bank_deposit/${selectedBank.value}/`)
      .then((res) => {
        deposits.value = []
        const results = res.data
        for (const item of results){
          deposits.value.push(makeItems(item))
        }
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  selectedDepositSimple.value = data
  intrRate.value = []
  intrRate2.value = []
  getDeposit()
  dialog.value = true
}

const getDeposit = function () {
  axios.get(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/`)
    .then((res) => {
      const data = res.data
      selectedDeposit.value = {
        '가입자 수 (MYFI 기준)': data.contract_user.length,
        '공시 제출월': data['dcls_month'],
        '금융 회사명': data['kor_co_nm'],
        '금융 상품명': data['name'],
        '가입 방법': data['join_way'],
        '만기 후 이자율': data['mtrt_int'],
        '우대 조건': data['spcl_cnd'],
        '가입 대상': data['join_member'],
        '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
        '최고 한도': data['max_limit'],
        '기타 유의사항': data['etc_note']
      }
      const optionList = data.depositoption_set

      if (Array.isArray(optionList)) {
        for (const option of optionList) {
          if (option.save_trm === "6") {
            intrRate.value[0] = option.intr_rate
            intrRate2.value[0] = option.intr_rate2
          } else if (option.save_trm === "12") {
            intrRate.value[1] = option.intr_rate
            intrRate2.value[1] = option.intr_rate2
          } else if (option.save_trm === "24") {
            intrRate.value[2] = option.intr_rate
            intrRate2.value[2] = option.intr_rate2
          } else if (option.save_trm === "36") {
            intrRate.value[3] = option.intr_rate
            intrRate2.value[3] = option.intr_rate2
          }
        }
      } else {
        console.warn('depositoption_set is not iterable:', optionList)
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const addDepositUser = function () {
  if (store.userInfo && store.userInfo.username) {
    axios.post(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/contract/`, null, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then((res) => {
        store.getUserInfo(store.userInfo.username)
        const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
        if (answer) {
          router.push({ name: 'productManage', params: { username: store.userInfo.username } })
        }
      })
      .catch((err) => {
        console.log(err)
      })
  } else {
    console.error('User info is not available.')
  }
}

const deleteDepositUser = function () {
  if (store.userInfo && store.userInfo.username) {
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
  } else {
    console.error('User info is not available.')
  }
}
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
    </header>
    <hr class="my-3">

    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <h3>{{ selectedDeposit['금융 상품명'] }}</h3>
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

    <table v-if="depositLength !== 0" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width">{{ header.title }}</th>
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

.table th, .table td {
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
