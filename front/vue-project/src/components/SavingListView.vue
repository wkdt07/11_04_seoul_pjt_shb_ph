<!-- <script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import BarChartDetail from '@/components/BarChartDetailView.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월 (Click to sort)', align: 'end', width: '12%', key: '6month' },
  { title: '12개월 (Click to sort)', align: 'end', width: '12%', key: '12month' },
  { title: '24개월 (Click to sort)', align: 'end', width: '12%', key: '24month' },
  { title: '36개월 (Click to sort)', align: 'end', width: '12%', key: '36month' },
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

const isContractDeposit = computed(() => {
  const userInfo = useCounterStore().userInfo
  return userInfo ? userInfo.contract_deposit.some(e => e['deposit_code'] === selectedDepositCode.value) : false
})

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

  return result
}

const getAllDeposit = function () {
  axios.get(`${store.DJANGO_URL}/financial/deposit_list/`)
    .then((res) => {
      const results = res.data
      deposits.value = results.map(item => makeItems(item))
      banks.value = ['전체 보기', ...new Set(results.map(item => item.kor_co_nm))]
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
        deposits.value = res.data.map(item => makeItems(item))
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
        '가입자 수 ': data.contract_user.length,
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
      }
      const optionList = data.options

      for (const option of optionList) {
        const idx = parseInt(option.save_trm) / 6 - 1
        if (idx >= 0 && idx < 4) {
          intrRate.value[idx] = option.intr_rate
          intrRate2.value[idx] = option.intr_rate2
        }
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const addDepositUser = function () {
  axios.post(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/contract/`, null, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
      const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
      if (answer) {
        router.push({ name: 'productManage', params: { username: store.userInfo.username } })
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteDepositUser = function () {
  axios.delete(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/contract/`, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
    })
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
          <BarChartDetail :title="selectedDepositSimple.name" :average-intr-rate="averageIntrRate" :intr-rate="intrRate"
            :intr-rate2="intrRate2" />
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
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width">{{ header.title }}
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

tbody>tr {
  transition: 200ms;
  cursor: pointer;
}

tbody>tr:hover {
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
}</style> -->
<!-- <template>
  <div>
    <header class="d-flex justify-space-between">
      <h1><span class="color">정기적금</span> 검색하기</h1>
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
        <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
        <div v-if="store.isLogin">
          <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
          <button v-else @click.prevent="addSavingUser">가입하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedSaving" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto">
          <BarChartDetail
            :title="selectedSavingSimple.name"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 적금 금리는 2023년 11월 기준입니다.</p>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>

        <div class="dialog-actions">
          <button @click="close">닫기</button>
        </div>
      </div>
    </div>

    <table v-if="savingLength !== 0" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
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

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import BarChartDetail from '@/components/BarChartDetailView.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월 (Click to sort)', align: 'end', width: '12%', key: '6month' },
  { title: '12개월 (Click to sort)', align: 'end', width: '12%', key: '12month' },
  { title: '24개월 (Click to sort)', align: 'end', width: '12%', key: '24month' },
  { title: '36개월 (Click to sort)', align: 'end', width: '12%', key: '36month' },
]

const savings = ref([])
const savingLength = computed(() => savings.value.length)
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedSavingSimple = ref(null)
const selectedSaving = ref(null)
const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
const dialog = ref(false)
const loading = ref(false)
const sortKey = ref('')
const sortOrder = ref(1) // 1: ascending, -1: descending

const averageIntrRate = [2.78, 3.62, 3.57, 3.52]
const intrRate = ref([null, null, null, null])
const intrRate2 = ref([null, null, null, null])

// const isContractSaving = computed(() => {
//   const userInfo = useCounterStore().userInfo
//   return userInfo ? userInfo.contract_saving.some(e => e['saving_code'] === selectedSavingCode.value) : false
// })
const isContractSaving = computed(() => {
  const userInfo = useCounterStore().userInfo;
  return userInfo && userInfo.contract_saving
    ? userInfo.contract_saving.some(e => e['saving_code'] === selectedSavingCode.value)
    : false;
});

const store = useCounterStore()
const router = useRouter()

const makeItems = function (item) {
  const result = {
    'saving_code': item['fin_prdt_cd'],
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

const getAllSaving = function () {
  loading.value = true
  axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
    .then((res) => {
      const results = res.data
      savings.value = results.map(item => makeItems(item))
      banks.value = ['전체 보기', ...new Set(results.map(item => item.kor_co_nm))]
      loading.value = false
    })
    .catch((err) => {
      console.log(err)
      loading.value = false
    })
}

onMounted(() => {
  getAllSaving()
})

const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllSaving()
  } else {
    loading.value = true
    axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
      .then((res) => {
        savings.value = res.data.map(item => makeItems(item))
        loading.value = false
      })
      .catch((err) => {
        console.log(err)
        loading.value = false
      })
  }
}

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  selectedSavingSimple.value = data
  intrRate.value = []
  intrRate2.value = []
  getSaving()
  dialog.value = true
}

// const getSaving = function () {
//   axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
//     .then((res) => {
//       const data = res.data
//       selectedSaving.value = {
//         '가입자 수 ': data.contract_user.length,
//         '공시 제출월': data['dcls_month'],
//         '금융 회사명': data['kor_co_nm'],
//         '금융 상품명': data['fin_prdt_nm'],
//         '가입 방법': data['join_way'],
//         '만기 후 이자율': data['mtrt_int'],
//         '우대 조건': data['spcl_cnd'],
//         '가입 대상': data['join_member'],
//         '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
//         '최고 한도': data['max_limit'],
//         '기타 유의사항': data['etc_note']
//       }
//       const optionList = data.options

//       for (const option of optionList) {
//         const idx = parseInt(option.save_trm) / 6 - 1
//         if (idx >= 0 && idx < 4) {
//           intrRate.value[idx] = option.intr_rate
//           intrRate2.value[idx] = option.intr_rate2
//         }
//       }
//     })
//     .catch((err) => {
//       console.log(err)
//     })
// }

const dataLoaded = ref(false);

const getSaving = function () {
  if (!selectedSavingCode.value) {
    console.error('selectedSavingCode is null or undefined');
    return;
  }

  axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
    .then((res) => {
      const data = res.data;
      selectedSaving.value = {
        '가입자 수 ': data.user_count,
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

      for (const option of optionList) {
        const idx = parseInt(option.save_trm) / 6 - 1;
        if (idx >= 0 && idx < 4) {
          intrRate.value[idx] = option.intr_rate;
          intrRate2.value[idx] = option.intr_rate2;
        }
        dataLoaded.value = true
      }
    })
    .catch((err) => {
      console.log(err);
      dataLoaded.value = false
    });
}


const addSavingUser = function () {
  axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
      const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
      if (answer) {
        router.push({ name: 'productManage', params: { username: store.userInfo.username } })
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteSavingUser = function () {
  axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
    })
}

const sort = function (key) {
  sortKey.value = key
  sortOrder.value *= -1

  savings.value.sort((a, b) => {
    if (a[key] < b[key]) return -1 * sortOrder.value
    if (a[key] > b[key]) return 1 * sortOrder.value
    return 0
  })
}

const reset = function () {
  selectedBank.value = '전체 보기'
  getAllSaving()
}
</script>

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

tbody>tr {
  transition: 200ms;
  cursor: pointer;
}

tbody>tr:hover {
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
</style> -->


<!-- ================================얘는 mm 확인 -->
<!-- <template>
  <div>
    <header class="d-flex justify-space-between">
      <h1><span class="color">정기적금</span> 검색하기</h1>
      <div class="w-25">
        <select v-model="selectedBank" @change="clickBank" class="ml-auto bank-select">
          <option v-for="bank in banks" :key="bank">{{ bank }}</option>
        </select>
      </div>
      <button @click="reset">리셋</button>
    </header>
    <hr class="my-3">

    <div>
    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
        <div v-if="store.isLogin">
          <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
          <button v-else @click.prevent="addSavingUser">가입하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedSaving" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto">
          <BarChartDetailSaving
            :title="selectedSavingSimple.name"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 적금 금리는 2023년 11월 기준입니다.</p>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>

        <div class="dialog-actions">
          <button @click="close">닫기</button>
        </div>
      </div>
    </div>
  </div>
    <table v-if="savingLength !== 0" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
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

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import BarChartDetail from '@/components/BarChartDetailView.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월 (Click to sort)', align: 'end', width: '12%', key: '6month' },
  { title: '12개월 (Click to sort)', align: 'end', width: '12%', key: '12month' },
  { title: '24개월 (Click to sort)', align: 'end', width: '12%', key: '24month' },
  { title: '36개월 (Click to sort)', align: 'end', width: '12%', key: '36month' },
]

const savings = ref([])
const savingLength = computed(() => savings.value.length)
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedSavingSimple = ref(null)
const selectedSaving = ref(null)
const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
const dialog = ref(false)
const loading = ref(false)
const sortKey = ref('')
const sortOrder = ref(1) // 1: ascending, -1: descending

const averageIntrRate = [2.78, 3.62, 3.57, 3.52]
const fixedIntrRate = ref([null, null, null, null])
const fixedIntrRate2 = ref([null, null, null, null])
const freeIntrRate = ref([null, null, null, null])
const freeIntrRate2 = ref([null, null, null, null])

const isContractSaving = computed(() => {
  const userInfo = useCounterStore().userInfo;
  
  if (!userInfo) {
    console.error("userInfo is undefined");
    return false;
  }
  
  const contractSavingArray = Array.isArray(userInfo.savings) ? userInfo.savings : [];
  return contractSavingArray.some(e => e['fin_prdt_cd'] === selectedSavingCode.value);
});

const store = useCounterStore()
const router = useRouter()

const makeItems = function (item) {
  const options = Array.isArray(item.options) ? item.options : []
  const result = {
    'saving_code': item['fin_prdt_cd'],
    'dcls_month': item['dcls_month'],
    'kor_co_nm': item['kor_co_nm'],
    'name': item['fin_prdt_nm'],
    '6month': null,
    '12month': null,
    '24month': null,
    '36month': null,
  }

  for (const option of options) {
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

const getAllSaving = function () {
  loading.value = true
  axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
    .then((res) => {
      const results = res.data
      savings.value = results.map(item => makeItems(item))
      banks.value = ['전체 보기', ...new Set(results.map(item => item.kor_co_nm))]
      loading.value = false
    })
    .catch((err) => {
      console.log(err)
      loading.value = false
    })
}

onMounted(() => {
  getAllSaving()
})

const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllSaving()
  } else {
    loading.value = true
    axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
      .then((res) => {
        savings.value = res.data.map(item => makeItems(item))
        loading.value = false
      })
      .catch((err) => {
        console.log(err)
        loading.value = false
      })
  }
}

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  selectedSavingSimple.value = data
  fixedIntrRate.value = []
  fixedIntrRate2.value = []
  freeIntrRate.value = []
  freeIntrRate2.value = []
  getSaving()
  dialog.value = true
}

const dataLoaded = ref(false);

const getSaving = function () {
  if (!selectedSavingCode.value) {
    console.error('selectedSavingCode is null or undefined');
    return;
  }

  axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
    .then((res) => {
      const data = res.data;
      selectedSaving.value = {
        '가입자 수': data.user_count,
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
      const fixedOptionList = data.fixed_options;
      const freeOptionList = data.free_options;

      fixedIntrRate.value = [null, null, null, null, null];
      fixedIntrRate2.value = [null, null, null, null, null];
      freeIntrRate.value = [null, null, null, null, null];
      freeIntrRate2.value = [null, null, null, null, null];

      for (const option of fixedOptionList) {
        const idx = parseInt(option.save_trm) / 6 - 1;
        if (idx >= 0 && idx < 5) {
          fixedIntrRate.value[idx] = option.intr_rate;
          fixedIntrRate2.value[idx] = option.intr_rate2;
        }
      }
      for (const option of freeOptionList) {
        const idx = parseInt(option.save_trm) / 6 - 1;
        if (idx >= 0 && idx < 5) {
          freeIntrRate.value[idx] = option.intr_rate;
          freeIntrRate2.value[idx] = option.intr_rate2;
        }
      }
      dataLoaded.value = true;
    })
    .catch((err) => {
      console.log(err);
      dataLoaded.value = false;
    });
}

const addSavingUser = function () {
  axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
      const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
      if (answer) {
        router.push({ name: 'productManage', params: { username: store.userInfo.username } })
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteSavingUser = function () {
  axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
    })
}

const sort = function (key) {
  sortKey.value = key
  sortOrder.value *= -1

  savings.value.sort((a, b) => {
    if (a[key] < b[key]) return -1 * sortOrder.value
    if (a[key] > b[key]) return 1 * sortOrder.value
    return 0
  })
}

const reset = function () {
  selectedBank.value = '전체 보기'
  getAllSaving()
}
</script>

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

tbody>tr {
  transition: 200ms;
  cursor: pointer;
}

tbody>tr:hover {
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
 -->
 <!-- <template>
  <div>
    <header class="d-flex justify-space-between">
      <h1><span class="color">정기적금</span> 검색하기</h1>
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
        <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
        <div v-if="store.isLogin">
          <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
          <button v-else @click.prevent="addSavingUser">가입하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedSaving" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto" v-if="dataLoaded"> <!-- 데이터가 로드된 경우에만 차트 렌더링 -->
          <!-- <BarChartDetail
            :title="selectedSavingSimple.name"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 적금 금리는 2023년 11월 기준입니다.</p>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>

        <div class="dialog-actions">
          <button @click="close">닫기</button>
        </div>
      </div>
    </div>

    <table v-if="savingLength !== 0" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
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

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import BarChartDetail from '@/components/BarChartDetailView.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월 (Click to sort)', align: 'end', width: '12%', key: '6month' },
  { title: '12개월 (Click to sort)', align: 'end', width: '12%', key: '12month' },
  { title: '24개월 (Click to sort)', align: 'end', width: '12%', key: '24month' },
  { title: '36개월 (Click to sort)', align: 'end', width: '12%', key: '36month' },
]

const savings = ref([])
const savingLength = computed(() => savings.value.length)
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedSavingSimple = ref(null)
const selectedSaving = ref(null)
const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
const dialog = ref(false)
const loading = ref(false)
const sortKey = ref('')
const sortOrder = ref(1) // 1: ascending, -1: descending

const averageIntrRate = [2.78, 3.62, 3.57, 3.52]
const intrRate = ref([null, null, null, null])
const intrRate2 = ref([null, null, null, null])

// const isContractSaving = computed(() => {
//   const userInfo = useCounterStore().userInfo;
//   return userInfo && userInfo.savings
//     ? userInfo.savings.some(e => e['saving_code'] === selectedSavingCode.value)
//     : false;
// });

const isContractSaving = computed(() => {
  const userInfo = useCounterStore().userInfo;
  
  // userInfo가 정의되어 있는지 확인
  if (!userInfo) {
    console.error("userInfo is undefined");
    return false;
  }
  
  // userInfo.contract_deposit가 배열인지 확인
  const contractSavingArray = Array.isArray(userInfo.savings) ? userInfo.savings : [];
  console.log()
  return contractSavingArray.some(e => e['fin_prdt_cd'] === selectedSavingCode.value);
});
const store = useCounterStore()
const router = useRouter()

const makeItems = function (item) {
  const result = {
    'saving_code': item['fin_prdt_cd'],
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
      console.log("24개월 금리:",result['24month'])
    } else if (saveTrm === "36") {
      result['36month'] = option['intr_rate']
      
    }
  }

  return result
}

const getAllSaving = function () {
  loading.value = true
  axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
    .then((res) => {
      const results = res.data
      savings.value = results.map(item => makeItems(item))
      banks.value = ['전체 보기', ...new Set(results.map(item => item.kor_co_nm))]
      loading.value = false
      console.log("적금에서 받아온 데이터",results)
    })
    .catch((err) => {
      console.log(err)
      loading.value = false
    })
}

onMounted(() => {
  getAllSaving()
})

const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllSaving()
  } else {
    loading.value = true
    axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
      .then((res) => {
        savings.value = res.data.map(item => makeItems(item))
        loading.value = false
      })
      .catch((err) => {
        console.log(err)
        loading.value = false
      })
  }
}

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  selectedSavingSimple.value = data
  intrRate.value = []
  intrRate2.value = []
  dataLoaded.value = false  // 클릭 시 로딩 상태 초기화
  getSaving()
  dialog.value = true
}

const dataLoaded = ref(false); -->
<!--
// const getSaving = function () {
//   if (!selectedSavingCode.value) {
//     console.error('selectedSavingCode is null or undefined');
//     return;
//   }

//   axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
//     .then((res) => {
//       const data = res.data;
//       selectedSaving.value = {
//         '가입자 수 ': data.user_count,
//         '공시 제출월': data['dcls_month'],
//         '금융 회사명': data['kor_co_nm'],
//         '금융 상품명': data['fin_prdt_nm'],
//         '가입 방법': data['join_way'],
//         '만기 후 이자율': data['mtrt_int'],
//         '우대 조건': data['spcl_cnd'],
//         '가입 대상': data['join_member'],
//         '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
//         '최고 한도': data['max_limit'],
//         '기타 유의사항': data['etc_note']
//       };
//       const optionList = data.options;

//       for (const option of optionList) {
//         const idx = parseInt(option.save_trm) / 6 - 1;
//         if (idx >= 0 && idx < 4) {
//           intrRate.value[idx] = option.intr_rate;
//           intrRate2.value[idx] = option.intr_rate2;
//         }
//       }
//       dataLoaded.value = true;  // 데이터 로드 완료
//     })
//     .catch((err) => {
//       console.log(err);
//       dataLoaded.value = false;
//     });
// }

// const getSaving = function () {
//   if (!selectedSavingCode.value) {
//     console.error('selectedSavingCode is null or undefined');
//     return;
//   }

//   axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
//     .then((res) => {
//       const data = res.data;
//       console.log(data)
//       selectedSaving.value = {
//         '가입자 수 ': data.user_count,
//         '공시 제출월': data['dcls_month'],
//         '금융 회사명': data['kor_co_nm'],
//         '금융 상품명': data['fin_prdt_nm'],
//         '가입 방법': data['join_way'],
//         '만기 후 이자율': data['mtrt_int'],
//         '우대 조건': data['spcl_cnd'],
//         '가입 대상': data['join_member'],
//         '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
//         '최고 한도': data['max_limit'],
//         '기타 유의사항': data['etc_note']
//       };
//       const optionList = data.options;

//       // 초기화
//       intrRate.value = [null, null, null, null];
//       intrRate2.value = [null, null, null, null];

//       // 옵션 리스트 순회하면서 인덱스 계산 및 값 설정
//       for (const option of optionList) {
//         const saveTrm = parseInt(option.save_trm);  // save_trm 값을 숫자로 변환
//         let idx = -1;
        
//         // saveTrm 값에 따른 인덱스 설정
//         switch (saveTrm) {
//           case 6:
//             idx = 0;
//             break;
//           case 12:
//             idx = 1;
//             break;
//           case 24:
//             idx = 2;
//             break;
//           case 36:
//             idx = 3;
//             break;
//           default:
//             console.warn(`Unexpected save_trm value: ${saveTrm}`);
//         }

//         if (idx >= 0 && idx < 4) {
//           intrRate.value[idx] = option.intr_rate;
//           intrRate2.value[idx] = option.intr_rate2;
//         }
//       }
//       dataLoaded.value = true;  // 데이터 로드 완료
//     })
//     .catch((err) => {
//       console.log(err);
//       dataLoaded.value = false;
//     });
// }


// const getSaving = function () {
//   if (!selectedSavingCode.value) {
//     console.error('selectedSavingCode is null or undefined');
//     return;
//   }

//   axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
//     .then((res) => {
//       const data = res.data;
//       console.log(data);
//       selectedSaving.value = {
//         '가입자 수 ': data.user_count,
//         '공시 제출월': data['dcls_month'],
//         '금융 회사명': data['kor_co_nm'],
//         '금융 상품명': data['fin_prdt_nm'],
//         '가입 방법': data['join_way'],
//         '만기 후 이자율': data['mtrt_int'],
//         '우대 조건': data['spcl_cnd'],
//         '가입 대상': data['join_member'],
//         '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
//         '최고 한도': data['max_limit'],
//         '기타 유의사항': data['etc_note']
//       };
//       const optionList = data.options;

//       // 초기화
//       intrRate.value = { 정액적립식: [null, null, null, null], 자유적립식: [null, null, null, null] };
//       intrRate2.value = { 정액적립식: [null, null, null, null], 자유적립식: [null, null, null, null] };

//       // 옵션 리스트 순회하면서 인덱스 계산 및 값 설정
//       for (const option of optionList) {
//         const saveTrm = parseInt(option.save_trm);  // save_trm 값을 숫자로 변환
//         const rsrvType = option.rsrv_type_nm;  // 적립 유형 (정액적립식/자유적립식)
        
//         let idx = -1;
//         // saveTrm 값에 따른 인덱스 설정
//         switch (saveTrm) {
//           case 6:
//             idx = 0;
//             break;
//           case 12:
//             idx = 1;
//             break;
//           case 24:
//             idx = 2;
//             break;
//           case 36:
//             idx = 3;
//             break;
//           default:
//             console.warn(`Unexpected save_trm value: ${saveTrm}`);
//         }

//         if (idx >= 0 && idx < 4) {
//           if (rsrvType === '정액적립식' || rsrvType === '자유적립식') {
//             intrRate.value[rsrvType][idx] = option.intr_rate;
//             intrRate2.value[rsrvType][idx] = option.intr_rate2;
//           } else {
//             console.warn(`Unexpected rsrv_type value: ${rsrvType}`);
//           }
//         }
//       }
//       dataLoaded.value = true;  // 데이터 로드 완료

//       // 데이터 변환
//       const chartData = transformData('saving', intrRate.value);
//       barChartData.value = chartData; // barChartData는 BarChartDetail 컴포넌트에 전달될 데이터
//     })
//     .catch((err) => {
//       console.log(err);
//       dataLoaded.value = false;
//     });
// }



// const addSavingUser = function () {
//   axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
//     headers: { Authorization: `Token ${store.token}` }
//   })
//     .then(() => {
//       store.getUserInfo(store.userInfo.username)
//       const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
//       if (answer) {
//         router.push({ name: 'productManage', params: { username: store.userInfo.username } })
//       }
//     })
//     .catch((err) => {
//       console.log(err)
//     })
// }

// const deleteSavingUser = function () {
//   axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
//     headers: { Authorization: `Token ${store.token}` }
//   })
//     .then(() => {
//       store.getUserInfo(store.userInfo.username)
//     })
//     .catch((err) => {
//       console.log(err)
//     })
// }

// const sort = function (key) {
//   sortKey.value = key
//   sortOrder.value *= -1

//   savings.value.sort((a, b) => {
//     if (a[key] < b[key]) return -1 * sortOrder.value
//     if (a[key] > b[key]) return 1 * sortOrder.value
//     return 0
//   })
// }

// const reset = function () {
//   selectedBank.value = '전체 보기'
//   getAllSaving()
// }
// </script>

// <style scoped>
// .loading {
//   display: flex;
//   height: 80vh;
//   align-items: center;
//   justify-content: center;
// }

// .progress-circular {
//   width: 80px;
//   height: 80px;
//   border: 5px solid #1089FF;
//   border-radius: 50%;
//   border-top: 5px solid transparent;
//   animation: spin 1s linear infinite;
// }

// @keyframes spin {
//   0% {
//     transform: rotate(0deg);
//   }

//   100% {
//     transform: rotate(360deg);
//   }
// }

// .dialog {
//   position: fixed;
//   top: 0;
//   left: 0;
//   width: 100%;
//   height: 100%;
//   display: flex;
//   align-items: center;
//   justify-content: center;
//   background: rgba(0, 0, 0, 0.5);
// }

// .dialog-content {
//   background: white;
//   padding: 20px;
//   border-radius: 8px;
//   width: 800px;
//   max-width: 90%;
// }

// .dialog-actions {
//   display: flex;
//   justify-content: flex-end;
//   margin-top: 20px;
// }

// tbody>tr {
//   transition: 200ms;
//   cursor: pointer;
// }

// tbody>tr:hover {
//   background-color: rgb(247, 250, 253);
//   color: #1089FF;
// }

// .table {
//   width: 100%;
//   border-collapse: collapse;
//   margin-top: 20px;
// }

// .table th,
// .table td {
//   border: 1px solid #ddd;
//   padding: 8px;
// }

// .table th {
//   background-color: #f2f2f2;
//   text-align: left;
// }

// .bank-select {
//   padding: 10px;
//   border: 1px solid #1089FF;
//   border-radius: 4px;
// }
// </style> -->

<!-- 



<template>
  <div>
    <header class="d-flex justify-space-between">
      <h1><span class="color">정기적금</span> 검색하기</h1>
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
        <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
        <div v-if="store.isLogin">
          <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
          <button v-else @click.prevent="addSavingUser">가입하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedSaving" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto" v-if="dataLoaded">
     <BarChartDetail
            :title="selectedSavingSimple.name"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 적금 금리는 2023년 11월 기준입니다.</p>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>

        <div class="dialog-actions">
          <button @click="close">닫기</button>
        </div>
      </div>
    </div>

    <table v-if="savingLength !== 0" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
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
</template> -->

<!-- <script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import BarChartDetail from '@/components/BarChartDetailView.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월 (Click to sort)', align: 'end', width: '12%', key: '6month' },
  { title: '12개월 (Click to sort)', align: 'end', width: '12%', key: '12month' },
  { title: '24개월 (Click to sort)', align: 'end', width: '12%', key: '24month' },
  { title: '36개월 (Click to sort)', align: 'end', width: '12%', key: '36month' },
]

const savings = ref([])
const savingLength = computed(() => savings.value.length)
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedSavingSimple = ref(null)
const selectedSaving = ref(null)
const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
const dialog = ref(false)
const loading = ref(false)
const sortKey = ref('')
const sortOrder = ref(1) // 1: ascending, -1: descending

const averageIntrRate = [2.78, 3.62, 3.57, 3.52]
const intrRate = ref([null, null, null, null])
const intrRate2 = ref([null, null, null, null])

// const isContractSaving = computed(() => {
//   const userInfo = useCounterStore().userInfo;
//   return userInfo && userInfo.savings
//     ? userInfo.savings.some(e => e['saving_code'] === selectedSavingCode.value)
//     : false;
// });

const isContractSaving = computed(() => {
  const userInfo = useCounterStore().userInfo;
  
  // userInfo가 정의되어 있는지 확인
  if (!userInfo) {
    console.error("userInfo is undefined");
    return false;
  }
  
  // userInfo.contract_deposit가 배열인지 확인
  const contractSavingArray = Array.isArray(userInfo.savings) ? userInfo.savings : [];
  console.log()
  return contractSavingArray.some(e => e['fin_prdt_cd'] === selectedSavingCode.value);
});
const store = useCounterStore()
const router = useRouter()

const makeItems = function (item) {
  const result = {
    'saving_code': item['fin_prdt_cd'],
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
      console.log("24개월 금리:",result['24month'])
    } else if (saveTrm === "36") {
      result['36month'] = option['intr_rate']
      
    }
  }

  return result
}

const getAllSaving = function () {
  loading.value = true
  axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
    .then((res) => {
      const results = res.data
      savings.value = results.map(item => makeItems(item))
      banks.value = ['전체 보기', ...new Set(results.map(item => item.kor_co_nm))]
      loading.value = false
      console.log("적금에서 받아온 데이터",results)
    })
    .catch((err) => {
      console.log(err)
      loading.value = false
    })
}

onMounted(() => {
  getAllSaving()
})

const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllSaving()
  } else {
    loading.value = true
    axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
      .then((res) => {
        savings.value = res.data.map(item => makeItems(item))
        loading.value = false
      })
      .catch((err) => {
        console.log(err)
        loading.value = false
      })
  }
}

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  selectedSavingSimple.value = data
  intrRate.value = []
  intrRate2.value = []
  dataLoaded.value = false  // 클릭 시 로딩 상태 초기화
  getSaving()
  dialog.value = true
}

const dataLoaded = ref(false); -->
<!--

  // const getSaving = function () {
    //   if (!selectedSavingCode.value) {
      //     console.error('selectedSavingCode is null or undefined');
      //     return;
      //   }
      
      //   axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
      //     .then((res) => {
        //       const data = res.data;
        //       selectedSaving.value = {
          //         '가입자 수 ': data.user_count,
          //         '공시 제출월': data['dcls_month'],
          //         '금융 회사명': data['kor_co_nm'],
          //         '금융 상품명': data['fin_prdt_nm'],
          //         '가입 방법': data['join_way'],
          //         '만기 후 이자율': data['mtrt_int'],
          //         '우대 조건': data['spcl_cnd'],
          //         '가입 대상': data['join_member'],
          //         '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
          //         '최고 한도': data['max_limit'],
          //         '기타 유의사항': data['etc_note']
          //       };
          //       const optionList = data.options;
          
          //       for (const option of optionList) {
            //         const idx = parseInt(option.save_trm) / 6 - 1;
            //         if (idx >= 0 && idx < 4) {
              //           intrRate.value[idx] = option.intr_rate;
              //           intrRate2.value[idx] = option.intr_rate2;
              //         }
              //       }
              //       dataLoaded.value = true;  // 데이터 로드 완료
              //     })
              //     .catch((err) => {
                //       console.log(err);
                //       dataLoaded.value = false;
                //     });
                // }
                
                // const getSaving = function () {
                  //   if (!selectedSavingCode.value) {
                    //     console.error('selectedSavingCode is null or undefined');
                    //     return;
                    //   }
                    
                    //   axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
                    //     .then((res) => {
                      //       const data = res.data;
                      //       console.log(data)
                      //       selectedSaving.value = {
                        //         '가입자 수 ': data.user_count,
                        //         '공시 제출월': data['dcls_month'],
                        //         '금융 회사명': data['kor_co_nm'],
                        //         '금융 상품명': data['fin_prdt_nm'],
                        //         '가입 방법': data['join_way'],
                        //         '만기 후 이자율': data['mtrt_int'],
                        //         '우대 조건': data['spcl_cnd'],
                        //         '가입 대상': data['join_member'],
                        //         '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
                        //         '최고 한도': data['max_limit'],
                        //         '기타 유의사항': data['etc_note']
                        //       };
                        //       const optionList = data.options;
                        
                        //       // 초기화
                        //       intrRate.value = [null, null, null, null];
                        //       intrRate2.value = [null, null, null, null];
                        
                        //       // 옵션 리스트 순회하면서 인덱스 계산 및 값 설정
                        //       for (const option of optionList) {
                          //         const saveTrm = parseInt(option.save_trm);  // save_trm 값을 숫자로 변환
                          //         let idx = -1;
                          
                          //         // saveTrm 값에 따른 인덱스 설정
                          //         switch (saveTrm) {
                            //           case 6:
                            //             idx = 0;
                            //             break;
                            //           case 12:
                            //             idx = 1;
                            //             break;
                            //           case 24:
                            //             idx = 2;
                            //             break;
                            //           case 36:
                            //             idx = 3;
                            //             break;
                            //           default:
                            //             console.warn(`Unexpected save_trm value: ${saveTrm}`);
                            //         }
                            
                            //         if (idx >= 0 && idx < 4) {
                              //           intrRate.value[idx] = option.intr_rate;
                              //           intrRate2.value[idx] = option.intr_rate2;
                              //         }
                              //       }
                              //       dataLoaded.value = true;  // 데이터 로드 완료
                              //     })
                              //     .catch((err) => {
                                //       console.log(err);
                                //       dataLoaded.value = false;
                                //     });
                                // }
                                
                                
                                // const getSaving = function () {
                                  //   if (!selectedSavingCode.value) {
                                    //     console.error('selectedSavingCode is null or undefined');
                                    //     return;
                                    //   }
                                    
                                    //   axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
                                    //     .then((res) => {
                                      //       const data = res.data;
                                      //       console.log(data);
                                      //       selectedSaving.value = {
                                        //         '가입자 수 ': data.user_count,
                                        //         '공시 제출월': data['dcls_month'],
                                        //         '금융 회사명': data['kor_co_nm'],
                                        //         '금융 상품명': data['fin_prdt_nm'],
                                        //         '가입 방법': data['join_way'],
                                        //         '만기 후 이자율': data['mtrt_int'],
                                        //         '우대 조건': data['spcl_cnd'],
                                        //         '가입 대상': data['join_member'],
                                        //         '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
                                        //         '최고 한도': data['max_limit'],
                                        //         '기타 유의사항': data['etc_note']
                                        //       };
                                        //       const optionList = data.options;
                                        
                                        //       // 초기화
                                        //       intrRate.value = { 정액적립식: [null, null, null, null], 자유적립식: [null, null, null, null] };
                                        //       intrRate2.value = { 정액적립식: [null, null, null, null], 자유적립식: [null, null, null, null] };
                                        
                                        //       // 옵션 리스트 순회하면서 인덱스 계산 및 값 설정
                                        //       for (const option of optionList) {
                                          //         const saveTrm = parseInt(option.save_trm);  // save_trm 값을 숫자로 변환
                                          //         const rsrvType = option.rsrv_type_nm;  // 적립 유형 (정액적립식/자유적립식)
                                          
                                          //         let idx = -1;
                                          //         // saveTrm 값에 따른 인덱스 설정
                                          //         switch (saveTrm) {
                                            //           case 6:
                                            //             idx = 0;
                                            //             break;
                                            //           case 12:
                                            //             idx = 1;
                                            //             break;
                                            //           case 24:
                                            //             idx = 2;
                                            //             break;
                                            //           case 36:
                                            //             idx = 3;
                                            //             break;
                                            //           default:
                                            //             console.warn(`Unexpected save_trm value: ${saveTrm}`);
                                            //         }
                                            
                                            //         if (idx >= 0 && idx < 4) {
//           if (rsrvType === '정액적립식' || rsrvType === '자유적립식') {
//             intrRate.value[rsrvType][idx] = option.intr_rate;
//             intrRate2.value[rsrvType][idx] = option.intr_rate2;
//           } else {
  //             console.warn(`Unexpected rsrv_type value: ${rsrvType}`);
  //           }
  //         }
  //       }
  //       dataLoaded.value = true;  // 데이터 로드 완료
  
  //       // 데이터 변환
  //       const chartData = transformData('saving', intrRate.value);
  //       barChartData.value = chartData; // barChartData는 BarChartDetail 컴포넌트에 전달될 데이터
  //     })
  //     .catch((err) => {
    //       console.log(err);
    //       dataLoaded.value = false;
    //     });
    // }
    
    
    
    // const addSavingUser = function () {
      //   axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
        //     headers: { Authorization: `Token ${store.token}` }
        //   })
        //     .then(() => {
          //       store.getUserInfo(store.userInfo.username)
          //       const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
          //       if (answer) {
            //         router.push({ name: 'productManage', params: { username: store.userInfo.username } })
            //       }
            //     })
            //     .catch((err) => {
              //       console.log(err)
              //     })
              // }
              
              // const deleteSavingUser = function () {
                //   axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
                  //     headers: { Authorization: `Token ${store.token}` }
                  //   })
                  //     .then(() => {
                    //       store.getUserInfo(store.userInfo.username)
                    //     })
                    //     .catch((err) => {
                      //       console.log(err)
                      //     })
                      // }
                      
                      // const sort = function (key) {
                        //   sortKey.value = key
                        //   sortOrder.value *= -1
                        
                        //   savings.value.sort((a, b) => {
                          //     if (a[key] < b[key]) return -1 * sortOrder.value
//     if (a[key] > b[key]) return 1 * sortOrder.value
//     return 0
//   })
// }

// const reset = function () {
  //   selectedBank.value = '전체 보기'
  //   getAllSaving()
  // }
// </script>
 
{/* <style scoped>
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
  
  tbody>tr {
    transition: 200ms;
    cursor: pointer;
  }
  
  tbody>tr:hover {
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

-->
<!--

  <template>
    <div>
      <header class="d-flex justify-space-between">
        <h1><span class="color">정기적금</span> 검색하기</h1>
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
          <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
          <div v-if="store.isLogin">
          <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
          <button v-else @click.prevent="addSavingUser">가입하기</button>
        </div>
        
        <table>
          <tbody>
            <tr v-for="(value, key) in selectedSaving" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto" v-if="dataLoaded"> 
          <BarChartDetail
            :title="selectedSavingSimple.name"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 적금 금리는 2023년 11월 기준입니다.</p>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>

        <div class="dialog-actions">
          <button @click="close">닫기</button>
        </div>
      </div>
    </div>

    <table v-if="savingLength !== 0" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
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

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import BarChartDetail from '@/components/BarChartDetailView.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '6개월 (Click to sort)', align: 'end', width: '12%', key: '6month' },
  { title: '12개월 (Click to sort)', align: 'end', width: '12%', key: '12month' },
  { title: '24개월 (Click to sort)', align: 'end', width: '12%', key: '24month' },
  { title: '36개월 (Click to sort)', align: 'end', width: '12%', key: '36month' },
]

const savings = ref([])
const savingLength = computed(() => savings.value.length)
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedSavingSimple = ref(null)
const selectedSaving = ref(null)
const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
const dialog = ref(false)
const loading = ref(false)
const sortKey = ref('')
const sortOrder = ref(1) // 1: ascending, -1: descending

const averageIntrRate = [2.78, 3.62, 3.57, 3.52]
const intrRate = ref([null, null, null, null])
const intrRate2 = ref([null, null, null, null])

const isContractSaving = computed(() => {
  const userInfo = useCounterStore().userInfo;
  return userInfo && userInfo.contract_saving
    ? userInfo.contract_saving.some(e => e['saving_code'] === selectedSavingCode.value)
    : false;
});

const store = useCounterStore()
const router = useRouter()

const makeItems = function (item) {
  const result = {
    'saving_code': item['fin_prdt_cd'],
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

const getAllSaving = function () {
  loading.value = true
  axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
    .then((res) => {
      const results = res.data
      savings.value = results.map(item => makeItems(item))
      banks.value = ['전체 보기', ...new Set(results.map(item => item.kor_co_nm))]
      loading.value = false
    })
    .catch((err) => {
      console.log(err)
      loading.value = false
    })
}

onMounted(() => {
  getAllSaving()
})

const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllSaving()
  } else {
    loading.value = true
    axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
      .then((res) => {
        savings.value = res.data.map(item => makeItems(item))
        loading.value = false
      })
      .catch((err) => {
        console.log(err)
        loading.value = false
      })
  }
}

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  selectedSavingSimple.value = data
  intrRate.value = []
  intrRate2.value = []
  dataLoaded.value = false  // 클릭 시 로딩 상태 초기화
  getSaving()
  dialog.value = true
}

const dataLoaded = ref(false);

const getSaving = function () {
  if (!selectedSavingCode.value) {
    console.error('selectedSavingCode is null or undefined');
    return;
  }

  axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`)
    .then((res) => {
      const data = res.data;
      selectedSaving.value = {
        '가입자 수 (MYFI 기준)': data.user_count,
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

      for (const option of optionList) {
        const idx = parseInt(option.save_trm) / 6 - 1;
        if (idx >= 0 && idx < 4) {
          intrRate.value[idx] = option.intr_rate;
          intrRate2.value[idx] = option.intr_rate2;
        }
      }
      dataLoaded.value = true;  // 데이터 로드 완료
    })
    .catch((err) => {
      console.log(err);
      dataLoaded.value = false;
    });
}

const addSavingUser = function () {
  axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
      const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
      if (answer) {
        router.push({ name: 'productManage', params: { username: store.userInfo.username } })
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteSavingUser = function () {
  axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
    })
}

const sort = function (key) {
  sortKey.value = key
  sortOrder.value *= -1

  savings.value.sort((a, b) => {
    if (a[key] < b[key]) return -1 * sortOrder.value
    if (a[key] > b[key]) return 1 * sortOrder.value
    return 0
  })
}

const reset = function () {
  selectedBank.value = '전체 보기'
  getAllSaving()
}
</script>

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

tbody>tr {
  transition: 200ms;
  cursor: pointer;
}

tbody>tr:hover {
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
        -->
<!--

        <template>
          <div>
            <header class="d-flex justify-space-between">
              <h1><span class="color">적금</span> 검색하기</h1>
        
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
                <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
                <div v-if="store.isLogin">
                  <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
                  <button v-else @click.prevent="addSavingUser">가입하기</button>
                </div>
        
                <table>
                  <tbody>
                    <tr v-for="(value, key) in selectedSaving" :key="key">
                      <td width="28%" class="font-weight-bold">{{ key }}</td>
                      <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                      <td v-else>{{ value }}</td>
                    </tr>
                  </tbody>
                </table>
                <hr class="my-3">
                <div class="mx-auto">
                  <BarChartDetail
                    :title="selectedSavingSimple.name"
                    :average-intr-rate="averageIntrRate"
                    :intr-rate="intrRate"
                    :intr-rate2="intrRate2"
                  />
                  <p class="text-caption">* 개월별 평균 적금 금리는 2023년 11월 기준입니다.</p>
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
            <table v-else-if="savingLength !== 0" class="table">
              <thead>
                <tr>
                  <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
                    {{ header.title }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
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
        
        const savings = ref([])
        const savingLength = computed(() => savings.value.length)
        
        const banks = ref(['전체 보기'])
        const selectedBank = ref('전체 보기')
        const selectedSavingSimple = ref(null)
        const selectedSaving = ref(null)
        const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
        const dialog = ref(false)
        const loading = ref(false)
        const sortKey = ref('')
        const sortOrder = ref(1) // 1: ascending, -1: descending
        
        const averageIntrRate = [3.45, 4.08, 3.4, 3.35]
        const intrRate = ref([null, null, null, null])
        const intrRate2 = ref([null, null, null, null])
        
        const store = useCounterStore()
        const router = useRouter()
        
        const makeItems = function (item) {
          const result = {
            'saving_code': item['fin_prdt_cd'],
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
        
        const getAllSavings = function () {
          loading.value = true
          axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
            .then((res) => {
              const results = res.data || []
              savings.value = []  // 기존 데이터 초기화
              console.log(results)
              for (const item of results) {
                savings.value.push(makeItems(item))
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
            getAllSavings()
          } else {
            loading.value = true
            axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
              .then((res) => {
                savings.value = []
                const results = res.data
                for (const item of results) {
                  savings.value.push(makeItems(item))
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
        
          savings.value.sort((a, b) => {
            if (a[key] < b[key]) return -1 * sortOrder.value
            if (a[key] > b[key]) return 1 * sortOrder.value
            return 0
          })
        }
        
        const reset = function () {
          selectedBank.value = '전체 보기'
          getAllSavings()
        }
        
        const close = function () {
          dialog.value = false
        }
        
        const getSaving = async function () {
          if (!selectedSavingCode.value) {
            console.error('selectedSavingCode is null or undefined');
            return;
          }
        
          try {
            const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`);
            const data = res.data;
            console.log("Saving data:", data);  // 데이터 확인용 콘솔 로그 추가
            selectedSaving.value = {
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
          selectedSavingSimple.value = data;
          intrRate.value = [null, null, null, null];
          intrRate2.value = [null, null, null, null];
          await getSaving(); // getSaving이 완료될 때까지 기다림
          dialog.value = true;
        }
        
        const addSavingUser = function () {
          axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
            headers: {
              Authorization: `Token ${store.token}`
            }
          })
          .then((res) => {
              console.log(selectedSavingCode)
              store.getUserInfo(store.userInfo.username)
              const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
              if (answer) {
                router.push({ name: 'ProfileView', params: { username: store.userInfo.username } })
              }
            })
            .catch((err) => {
              console.log('뽑힌거:',selectedSavingCode.value)
              console.log(err)
            })
        }
        
        const deleteSavingUser = function () {
          axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
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
          getAllSavings();
        });
        </script>
        
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
      -->
       <!-- 
      <template>
        <div>
          <header class="d-flex justify-space-between">
            <h1><span class="color">적금</span> 검색하기</h1>
      
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
              <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
              <div v-if="store.isLogin">
                <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
                <button v-else @click.prevent="addSavingUser">가입하기</button>
              </div>
      
              <table>
                <tbody>
                  <tr v-for="(value, key) in selectedSaving" :key="key">
                    <td width="28%" class="font-weight-bold">{{ key }}</td>
                    <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                    <td v-else>{{ value }}</td>
                  </tr>
                </tbody>
              </table>
              <hr class="my-3">
              <div class="mx-auto">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name"
                  :average-intr-rate="averageIntrRate"
                  :intr-rate="intrRate"
                  :intr-rate2="intrRate2"
                  :saving-type="selectedSavingSimple.saving_type"
                />
                <p class="text-caption">* 개월별 평균 적금 금리는 2023년 11월 기준입니다.</p>
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
          <table v-else-if="savingLength !== 0" class="table">
            <thead>
              <tr>
                <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
                  {{ header.title }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
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
      
      <script setup>
      import { ref, onMounted, computed } from 'vue'
      import { useRouter } from 'vue-router'
      import { useCounterStore } from '../stores/counter'
      import BarChartDetailSaving from '@/components/BarChartDetailSaving.vue'
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
      
      const savings = ref([])
      const savingLength = computed(() => savings.value.length)
      
      const banks = ref(['전체 보기'])
      const selectedBank = ref('전체 보기')
      const selectedSavingSimple = ref(null)
      const selectedSaving = ref(null)
      const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
      const dialog = ref(false)
      const loading = ref(false)
      const sortKey = ref('')
      const sortOrder = ref(1) // 1: ascending, -1: descending
      
      const averageIntrRate = [3.45, 4.08, 3.4, 3.35]
      const intrRate = ref([null, null, null, null])
      const intrRate2 = ref([null, null, null, null])
      
      const store = useCounterStore()
      const router = useRouter()
      
      const makeItems = function (item) {
        const result = {
          'saving_code': item['fin_prdt_cd'],
          'dcls_month': item['dcls_month'],
          'kor_co_nm': item['kor_co_nm'],
          'name': item['fin_prdt_nm'],
          'saving_type': item['saving_type'],  // 자유적립형 또는 정기적금형
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
      
      const getAllSavings = function () {
        loading.value = true
        axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
          .then((res) => {
            const results = res.data || []
            savings.value = []  // 기존 데이터 초기화
            console.log(results)
            for (const item of results) {
              savings.value.push(makeItems(item))
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
          getAllSavings()
        } else {
          loading.value = true
          axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
            .then((res) => {
              savings.value = []
              const results = res.data
              for (const item of results) {
                savings.value.push(makeItems(item))
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
      
        savings.value.sort((a, b) => {
          if (a[key] < b[key]) return -1 * sortOrder.value
          if (a[key] > b[key]) return 1 * sortOrder.value
          return 0
        })
      }
      
      const reset = function () {
        selectedBank.value = '전체 보기'
        getAllSavings()
      }
      
      const close = function () {
        dialog.value = false
      }
      
      const getSaving = async function () {
        if (!selectedSavingCode.value) {
          console.error('selectedSavingCode is null or undefined');
          return;
        }
      
        try {
          const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`);
          const data = res.data;
          console.log("Saving data:", data);  // 데이터 확인용 콘솔 로그 추가
          selectedSaving.value = {
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
        selectedSavingSimple.value = data;
        intrRate.value = [null, null, null, null];
        intrRate2.value = [null, null, null, null];
        await getSaving(); // getSaving이 완료될 때까지 기다림
        dialog.value = true;
      }
      
      const addSavingUser = function () {
        axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
          headers: {
            Authorization: `Token ${store.token}`
          }
        })
        .then((res) => {
            console.log(selectedSavingCode)
            store.getUserInfo(store.userInfo.username)
            const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
            if (answer) {
              router.push({ name: 'ProfileView', params: { username: store.userInfo.username } })
            }
          })
          .catch((err) => {
            console.log('뽑힌거:',selectedSavingCode.value)
            console.log(err)
          })
      }
      
      const deleteSavingUser = function () {
        axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
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
        getAllSavings();
      });
      </script>
      
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
    -->

    <!-- <template>
      <div>
        <header class="d-flex justify-space-between">
          <h1><span class="color">적금</span> 검색하기</h1>
    
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
            <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
            <div v-if="store.isLogin">
              <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
              <button v-else @click.prevent="addSavingUser">가입하기</button>
            </div>
    
            <table>
              <tbody>
                <tr v-for="(value, key) in selectedSaving" :key="key">
                  <td width="28%" class="font-weight-bold">{{ key }}</td>
                  <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                  <td v-else>{{ value }}</td>
                </tr>
              </tbody>
            </table>
            <hr class="my-3">
            <div class="mx-auto">
              <template v-if="savingType === 'F'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (자유적립형)'"
                  :intr-rate="intrRate"
                  :intr-rate2="intrRate2"
                  saving-type="자유적립형"
                />
              </template>
              <template v-if="savingType === 'S'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (정기적금형)'"
                  :intr-rate="intrRate"
                  :intr-rate2="intrRate2"
                  saving-type="정기적금형"
                />
              </template>
              <template v-if="savingType === 'BOTH'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (자유적립형)'"
                  :intr-rate="intrRateFreedom"
                  :intr-rate2="intrRate2Freedom"
                  saving-type="자유적립형"
                />
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (정기적금형)'"
                  :intr-rate="intrRateRegular"
                  :intr-rate2="intrRate2Regular"
                  saving-type="정기적금형"
                />
              </template>
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
        <table v-else-if="savingLength !== 0" class="table">
          <thead>
            <tr>
              <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
                {{ header.title }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
              <td>{{ item['dcls_month'] }}</td>
              <td>{{ item['kor_co_nm'] }}</td>
              <td align="center">{{ item['name'] }}</td>
              <td align="center">{{ item['max_intr_rate2'] }}</td>
            </tr>
          </tbody>
        </table>
    
        <div v-else class="loading">
          <div class="progress-circular"></div>
        </div>
      </div>
    </template>
    
    <script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useRouter } from 'vue-router'
    import { useCounterStore } from '../stores/counter'
    import BarChartDetailSaving from '@/components/BarChartDetailSaving.vue'
    import axios from 'axios'
    
    const headers = [
      { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
      { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
      { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
      { title: '최고우대금리', align: 'end', width: '12%', key: 'max_intr_rate2' },
    ]
    
    const savings = ref([])
    const savingLength = computed(() => savings.value.length)
    
    const banks = ref(['전체 보기'])
    const selectedBank = ref('전체 보기')
    const selectedSavingSimple = ref(null)
    const selectedSaving = ref(null)
    const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
    const dialog = ref(false)
    const loading = ref(false)
    const sortKey = ref('')
    const sortOrder = ref(1) // 1: ascending, -1: descending
    
    const intrRate = ref([])
    const intrRate2 = ref([])
    const intrRateFreedom = ref([])
    const intrRate2Freedom = ref([])
    const intrRateRegular = ref([])
    const intrRate2Regular = ref([])
    const savingType = ref('NONE');
    
    const store = useCounterStore()
    const router = useRouter()
    
    const makeItems = function (item) {
      const result = {
        'saving_code': item['fin_prdt_cd'],
        'dcls_month': item['dcls_month'],
        'kor_co_nm': item['kor_co_nm'],
        'name': item['fin_prdt_nm'],
        'max_intr_rate2': Math.max(...item.options.map(opt => opt.intr_rate2 || 0)),  // 최고우대금리
        'saving_type': item.options.some(opt => opt.rsrv_type === 'S') ? (item.options.some(opt => opt.rsrv_type === 'F') ? 'BOTH' : 'S') : 'F'  // 상품 타입
      }
    
      return result
    }
    const isContractSaving = computed(() => {
  const userInfo = useCounterStore().userInfo;

  if (!userInfo) {
    console.error("userInfo is undefined");
    return false;
  }

  const contractSavingArray = Array.isArray(userInfo.savings) ? userInfo.savings : [];
  return contractSavingArray.some(e => e['fin_prdt_cd'] === selectedSavingCode.value);
});
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
    
    const getAllSavings = function () {
      loading.value = true
      axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
        .then((res) => {
          const results = res.data || []
          savings.value = []  // 기존 데이터 초기화
          console.log(results)
          for (const item of results) {
            savings.value.push(makeItems(item))
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
        getAllSavings()
      } else {
        loading.value = true
        axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
          .then((res) => {
            savings.value = []
            const results = res.data
            for (const item of results) {
              savings.value.push(makeItems(item))
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
    
      savings.value.sort((a, b) => {
        if (a[key] < b[key]) return -1 * sortOrder.value
        if (a[key] > b[key]) return 1 * sortOrder.value
        return 0
      })
    }
    
    const reset = function () {
      selectedBank.value = '전체 보기'
      getAllSavings()
    }
    
    const close = function () {
      dialog.value = false
    }
    
    const getSaving = async function () {
  if (!selectedSavingCode.value) {
    console.error('selectedSavingCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`);
    const data = res.data;
    console.log("Saving data:", data);  // 데이터 확인용 콘솔 로그 추가

    const freedomOptions = data.options.filter(option => option.rsrv_type === 'F');
    const regularOptions = data.options.filter(option => option.rsrv_type === 'S');

    const freedomLabels = freedomOptions.map(option => `${option.save_trm}개월 금리`);
    const freedomRates = freedomOptions.map(option => option.intr_rate);
    const freedomRates2 = freedomOptions.map(option => option.intr_rate2);

    const regularLabels = regularOptions.map(option => `${option.save_trm}개월 금리`);
    const regularRates = regularOptions.map(option => option.intr_rate);
    const regularRates2 = regularOptions.map(option => option.intr_rate2);

    selectedSaving.value = {
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
      '기타 유의사항': data['etc_note'],
      'freedomLabels': freedomLabels.length ? freedomLabels : ['데이터 없음'],
      'freedomRates': freedomRates.length ? freedomRates : [0],
      'freedomRates2': freedomRates2.length ? freedomRates2 : [0],
      'regularLabels': regularLabels.length ? regularLabels : ['데이터 없음'],
      'regularRates': regularRates.length ? regularRates : [0],
      'regularRates2': regularRates2.length ? regularRates2 : [0]
    };

    intrRateFreedom.value = freedomRates.length ? freedomRates : [0];
    intrRate2Freedom.value = freedomRates2.length ? freedomRates2 : [0];
    intrRateRegular.value = regularRates.length ? regularRates : [0];
    intrRate2Regular.value = regularRates2.length ? regularRates2 : [0];

    if (freedomOptions.length && regularOptions.length) {
      savingType.value = 'BOTH'
    } else if (freedomOptions.length) {
      savingType.value = 'F'
    } else if (regularOptions.length) {
      savingType.value = 'S'
    } else {
      savingType.value = 'NONE'
    }

    console.log("freedomRates:", intrRateFreedom.value);
    console.log("freedomRates2:", intrRate2Freedom.value);
    console.log("regularRates:", intrRateRegular.value);
    console.log("regularRates2:", intrRate2Regular.value);
  } catch (err) {
    console.log(err);
  }
}


    
    const clickRow = async function (data) {
      selectedSavingSimple.value = data;
      await getSaving(); // getSaving이 완료될 때까지 기다림
      dialog.value = true;
    }
    
    const addSavingUser = function () {
      axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      .then((res) => {
          console.log(selectedSavingCode)
          store.getUserInfo(store.userInfo.username)
          const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
          if (answer) {
            router.push({ name: 'ProfileView', params: { username: store.userInfo.username } })
          }
        })
        .catch((err) => {
          console.log('뽑힌거:',selectedSavingCode.value)
          console.log(err)
        })
    }
    
    const deleteSavingUser = function () {
      axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
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
      getAllSavings();
    });
    </script>
    
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
    </style> -->
<!--     
    <template>
      <div>
        <header class="d-flex justify-space-between">
          <h1><span class="color">적금</span> 검색하기</h1>
    
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
            <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
            <div v-if="store.isLogin">
              <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
              <button v-else @click.prevent="addSavingUser">가입하기</button>
            </div>
    
            <table>
              <tbody>
                <tr v-for="(value, key) in selectedSaving" :key="key">
                  <td width="28%" class="font-weight-bold">{{ key }}</td>
                  <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                  <td v-else>{{ value }}</td>
                </tr>
              </tbody>
            </table>
            <hr class="my-3">
            <div class="mx-auto">
              <template v-if="savingType === 'F'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (자유적립형)'"
                  :labels="selectedSaving.freedomLabels"
                  :intr-rate="intrRateFreedom"
                  :intr-rate2="intrRate2Freedom"
                  saving-type="자유적립형"
                />
              </template>
              <template v-else-if="savingType === 'S'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (정기적금형)'"
                  :labels="selectedSaving.regularLabels"
                  :intr-rate="intrRateRegular"
                  :intr-rate2="intrRate2Regular"
                  saving-type="정기적금형"
                />
              </template>
              <template v-else-if="savingType === 'BOTH'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (자유적립형)'"
                  :labels="selectedSaving.freedomLabels"
                  :intr-rate="intrRateFreedom"
                  :intr-rate2="intrRate2Freedom"
                  saving-type="자유적립형"
                />
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (정기적금형)'"
                  :labels="selectedSaving.regularLabels"
                  :intr-rate="intrRateRegular"
                  :intr-rate2="intrRate2Regular"
                  saving-type="정기적금형"
                />
              </template>
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
        <table v-else-if="savingLength !== 0" class="table">
          <thead>
            <tr>
              <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
                {{ header.title }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
              <td>{{ item['dcls_month'] }}</td>
              <td>{{ item['kor_co_nm'] }}</td>
              <td align="center">{{ item['name'] }}</td>
              <td align="center">{{ item['max_intr_rate2'] }}</td>
            </tr>
          </tbody>
        </table>
    
        <div v-else class="loading">
          <div class="progress-circular"></div>
        </div>
      </div>
    </template>
    
    <script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useRouter } from 'vue-router'
    import { useCounterStore } from '../stores/counter'
    import BarChartDetailSaving from '@/components/BarChartDetailSaving.vue'
    import axios from 'axios'
    
    const headers = [
      { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
      { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
      { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
      { title: '최고우대금리', align: 'end', width: '12%', key: 'max_intr_rate2' },
    ]
    
    const savings = ref([])
    const savingLength = computed(() => savings.value.length)
    
    const banks = ref(['전체 보기'])
    const selectedBank = ref('전체 보기')
    const selectedSavingSimple = ref(null)
    const selectedSaving = ref(null)
    const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
    const dialog = ref(false)
    const loading = ref(false)
    const sortKey = ref('')
    const sortOrder = ref(1) // 1: ascending, -1: descending
    
    const intrRateFreedom = ref([])
    const intrRate2Freedom = ref([])
    const intrRateRegular = ref([])
    const intrRate2Regular = ref([])
    
    const savingType = ref('NONE')
    
    const isContractSaving = computed(() => {
      const userInfo = useCounterStore().userInfo;
      
      if (!userInfo) {
        console.error("userInfo is undefined");
        return false;
      }
      
      const contractSavingArray = Array.isArray(userInfo.savings) ? userInfo.savings : [];
      return contractSavingArray.some(e => e['fin_prdt_cd'] === selectedSavingCode.value);
    });
    
    const store = useCounterStore()
    const router = useRouter()
    
    const makeItems = function (item) {
      const result = {
        'saving_code': item['fin_prdt_cd'],
        'dcls_month': item['dcls_month'],
        'kor_co_nm': item['kor_co_nm'],
        'name': item['fin_prdt_nm'],
        'max_intr_rate2': Math.max(...item.options.map(opt => opt.intr_rate2 || 0)),  // 최고우대금리
        'saving_type': item.options.some(opt => opt.rsrv_type === 'S') ? (item.options.some(opt => opt.rsrv_type === 'F') ? 'BOTH' : 'S') : 'F'  // 상품 타입
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
    
    const getAllSavings = function () {
      loading.value = true
      axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
        .then((res) => {
          const results = res.data || []
          savings.value = []  // 기존 데이터 초기화
          console.log(results)
          for (const item of results) {
            savings.value.push(makeItems(item))
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
        getAllSavings()
      } else {
        loading.value = true
        axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
          .then((res) => {
            savings.value = []
            const results = res.data
            for (const item of results) {
              savings.value.push(makeItems(item))
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
    
      savings.value.sort((a, b) => {
        if (a[key] < b[key]) return -1 * sortOrder.value
        if (a[key] > b[key]) return 1 * sortOrder.value
        return 0
      })
    }
    
    const reset = function () {
      selectedBank.value = '전체 보기'
      getAllSavings()
    }
    
    const close = function () {
      dialog.value = false
    }
    
    const getSaving = async function () {
      if (!selectedSavingCode.value) {
        console.error('selectedSavingCode is null or undefined');
        return;
      }
    
      try {
        const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`);
        const data = res.data;
        console.log("Saving data:", data);  // 데이터 확인용 콘솔 로그 추가
    
        const freedomOptions = data.options.filter(option => option.rsrv_type === 'F');
        const regularOptions = data.options.filter(option => option.rsrv_type === 'S');
    
        const freedomLabels = freedomOptions.map(option => `${option.save_trm}개월 금리`);
        const freedomRates = freedomOptions.map(option => option.intr_rate);
        const freedomRates2 = freedomOptions.map(option => option.intr_rate2);
    
        const regularLabels = regularOptions.map(option => `${option.save_trm}개월 금리`);
        const regularRates = regularOptions.map(option => option.intr_rate);
        const regularRates2 = regularOptions.map(option => option.intr_rate2);
    
        selectedSaving.value = {
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
          '기타 유의사항': data['etc_note'],
          'freedomLabels': freedomLabels.length ? freedomLabels : ['데이터 없음'],
          'freedomRates': freedomRates.length ? freedomRates : [0],
          'freedomRates2': freedomRates2.length ? freedomRates2 : [0],
          'regularLabels': regularLabels.length ? regularLabels : ['데이터 없음'],
          'regularRates': regularRates.length ? regularRates : [0],
          'regularRates2': regularRates2.length ? regularRates2 : [0]
        };
    
        intrRateFreedom.value = freedomRates.length ? freedomRates : [0];
        intrRate2Freedom.value = freedomRates2.length ? freedomRates2 : [0];
        intrRateRegular.value = regularRates.length ? regularRates : [0];
        intrRate2Regular.value = regularRates2.length ? regularRates2 : [0];
    
        if (freedomOptions.length && regularOptions.length) {
          savingType.value = 'BOTH'
        } else if (freedomOptions.length) {
          savingType.value = 'F'
        } else if (regularOptions.length) {
          savingType.value = 'S'
        } else {
          savingType.value = 'NONE'
        }
    
        console.log("freedomRates:", intrRateFreedom.value);
        console.log("freedomRates2:", intrRate2Freedom.value);
        console.log("regularRates:", intrRateRegular.value);
        console.log("regularRates2:", intrRate2Regular.value);
      } catch (err) {
        console.log(err);
      }
    }
    
    const clickRow = async function (data) {
      selectedSavingSimple.value = data;
      await getSaving(); // getSaving이 완료될 때까지 기다림
      dialog.value = true;
    }
    
    const addSavingUser = function () {
      axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      .then((res) => {
          console.log(selectedSavingCode)
          store.getUserInfo(store.userInfo.username)
          const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
          if (answer) {
            router.push({ name: 'ProfileView', params: { username: store.userInfo.username } })
          }
        })
        .catch((err) => {
          console.log('뽑힌거:',selectedSavingCode.value)
          console.log(err)
        })
    }
    
    const deleteSavingUser = function () {
      axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
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
      getAllSavings();
    });
    </script>
    
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
     -->


<!-- 
     <template>
      <div>
        <header class="d-flex justify-space-between">
          <h1><span class="color">적금</span> 검색하기</h1>
    
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
            <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
            <div v-if="store.isLogin">
              <button v-if="isContractSaving" @click.prevent="deleteSavingUser">가입 취소하기</button>
              <button v-else @click.prevent="addSavingUser">가입하기</button>
            </div>
    
            <table>
              <tbody>
                <tr v-for="(value, key) in selectedSaving" :key="key">
                  <td width="28%" class="font-weight-bold">{{ key }}</td>
                  <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                  <td v-else>{{ value }}</td>
                </tr>
              </tbody>
            </table>
            <hr class="my-3">
            <div class="mx-auto">
              <div v-if="savingType === 'F'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (자유적립형)'"
                  :labels="selectedSaving.freedomLabels"
                  :intr-rate="intrRateFreedom"
                  :intr-rate2="intrRate2Freedom"
                  saving-type="자유적립형"
                />
              </div>
              <div v-else-if="savingType === 'S'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (정기적금형)'"
                  :labels="selectedSaving.regularLabels"
                  :intr-rate="intrRateRegular"
                  :intr-rate2="intrRate2Regular"
                  saving-type="정기적금형"
                />
              </div>
              <div v-else-if="savingType === 'BOTH'">
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (자유적립형)'"
                  :labels="selectedSaving.freedomLabels"
                  :intr-rate="intrRateFreedom"
                  :intr-rate2="intrRate2Freedom"
                  saving-type="자유적립형"
                />
                <BarChartDetailSaving
                  :title="selectedSavingSimple.name + ' (정기적금형)'"
                  :labels="selectedSaving.regularLabels"
                  :intr-rate="intrRateRegular"
                  :intr-rate2="intrRate2Regular"
                  saving-type="정기적금형"
                />
              </div>
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
        <table v-else-if="savingLength !== 0" class="table">
          <thead>
            <tr>
              <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width" @click="sort(header.key)">
                {{ header.title }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
              <td>{{ item['dcls_month'] }}</td>
              <td>{{ item['kor_co_nm'] }}</td>
              <td align="center">{{ item['name'] }}</td>
              <td align="center">{{ item['max_intr_rate2'] }}</td>
            </tr>
          </tbody>
        </table>
    
        <div v-else class="loading">
          <div class="progress-circular"></div>
        </div>
      </div>
    </template>
    
    <script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useRouter } from 'vue-router'
    import { useCounterStore } from '../stores/counter'
    import BarChartDetailSaving from '@/components/BarChartDetailSaving.vue'
    import axios from 'axios'
    
    const headers = [
      { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
      { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
      { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
      { title: '최고우대금리', align: 'end', width: '12%', key: 'max_intr_rate2' },
    ]
    
    const savings = ref([])
    const savingLength = computed(() => savings.value.length)
    
    const banks = ref(['전체 보기'])
    const selectedBank = ref('전체 보기')
    const selectedSavingSimple = ref(null)
    const selectedSaving = ref(null)
    const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
    const dialog = ref(false)
    const loading = ref(false)
    const sortKey = ref('')
    const sortOrder = ref(1) // 1: ascending, -1: descending
    
    const intrRateFreedom = ref([])
    const intrRate2Freedom = ref([])
    const intrRateRegular = ref([])
    const intrRate2Regular = ref([])
    
    const savingType = ref('NONE')
    
    const isContractSaving = computed(() => {
      const userInfo = useCounterStore().userInfo;
      
      if (!userInfo) {
        console.error("userInfo is undefined");
        return false;
      }
      
      const contractSavingArray = Array.isArray(userInfo.savings) ? userInfo.savings : [];
      return contractSavingArray.some(e => e['fin_prdt_cd'] === selectedSavingCode.value);
    });
    
    const store = useCounterStore()
    const router = useRouter()
    
    const makeItems = function (item) {
      const result = {
        'saving_code': item['fin_prdt_cd'],
        'dcls_month': item['dcls_month'],
        'kor_co_nm': item['kor_co_nm'],
        'name': item['fin_prdt_nm'],
        'max_intr_rate2': Math.max(...item.options.map(opt => opt.intr_rate2 || 0)),  // 최고우대금리
        'saving_type': item.options.some(opt => opt.rsrv_type === 'S') ? (item.options.some(opt => opt.rsrv_type === 'F') ? 'BOTH' : 'S') : 'F'  // 상품 타입
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
    
    const getAllSavings = function () {
      loading.value = true
      axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
        .then((res) => {
          const results = res.data || []
          savings.value = []  // 기존 데이터 초기화
          console.log(results)
          for (const item of results) {
            savings.value.push(makeItems(item))
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
        getAllSavings()
      } else {
        loading.value = true
        axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
          .then((res) => {
            savings.value = []
            const results = res.data
            for (const item of results) {
              savings.value.push(makeItems(item))
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
    
      savings.value.sort((a, b) => {
        if (a[key] < b[key]) return -1 * sortOrder.value
        if (a[key] > b[key]) return 1 * sortOrder.value
        return 0
      })
    }
    
    const reset = function () {
      selectedBank.value = '전체 보기'
      getAllSavings()
    }
    
    const close = function () {
      dialog.value = false
    }
    
    const getSaving = async function () {
      if (!selectedSavingCode.value) {
        console.error('selectedSavingCode is null or undefined');
        return;
      }
    
      try {
        const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`);
        const data = res.data;
        console.log("Saving data:", data);  // 데이터 확인용 콘솔 로그 추가
    
        const freedomOptions = data.options.filter(option => option.rsrv_type === 'F');
        const regularOptions = data.options.filter(option => option.rsrv_type === 'S');
    
        const freedomLabels = freedomOptions.map(option => `${option.save_trm}개월 금리`);
        const freedomRates = freedomOptions.map(option => option.intr_rate);
        const freedomRates2 = freedomOptions.map(option => option.intr_rate2);
    
        const regularLabels = regularOptions.map(option => `${option.save_trm}개월 금리`);
        const regularRates = regularOptions.map(option => option.intr_rate);
        const regularRates2 = regularOptions.map(option => option.intr_rate2);
    
        selectedSaving.value = {
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
          '기타 유의사항': data['etc_note'],
          'freedomLabels': freedomLabels.length ? freedomLabels : ['데이터 없음'],
          'freedomRates': freedomRates.length ? freedomRates : [0],
          'freedomRates2': freedomRates2.length ? freedomRates2 : [0],
          'regularLabels': regularLabels.length ? regularLabels : ['데이터 없음'],
          'regularRates': regularRates.length ? regularRates : [0],
          'regularRates2': regularRates2.length ? regularRates2 : [0]
        };
    
        intrRateFreedom.value = freedomRates.length ? freedomRates : [0];
        intrRate2Freedom.value = freedomRates2.length ? freedomRates2 : [0];
        intrRateRegular.value = regularRates.length ? regularRates : [0];
        intrRate2Regular.value = regularRates2.length ? regularRates2 : [0];
    
        if (freedomOptions.length && regularOptions.length) {
          savingType.value = 'BOTH'
        } else if (freedomOptions.length) {
          savingType.value = 'F'
        } else if (regularOptions.length) {
          savingType.value = 'S'
        } else {
          savingType.value = 'NONE'
        }
    
        console.log("freedomRates:", intrRateFreedom.value);
        console.log("freedomRates2:", intrRate2Freedom.value);
        console.log("regularRates:", intrRateRegular.value);
        console.log("regularRates2:", intrRate2Regular.value);
      } catch (err) {
        console.log(err);
      }
    }
    
    const clickRow = async function (data) {
      selectedSavingSimple.value = data;
      await getSaving(); // getSaving이 완료될 때까지 기다림
      dialog.value = true;
    }
    
    const addSavingUser = function () {
      axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      .then((res) => {
          console.log(selectedSavingCode)
          store.getUserInfo(store.userInfo.username)
          const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
          if (answer) {
            router.push({ name: 'ProfileView', params: { username: store.userInfo.username } })
          }
        })
        .catch((err) => {
          console.log('뽑힌거:',selectedSavingCode.value)
          console.log(err)
        })
    }
    
    const deleteSavingUser = function () {
      axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
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
      getAllSavings();
    });
    </script>
    
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
      width: 70%;
      max-width: 90%;
      max-height: 70%;
      overflow-y: auto;
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
     -->




<template>
  <div>
    <header class="d-flex justify-space-between header-style">
      <h1><span class="color">정기적금</span> 검색하기</h1>

      <div class="search-container">
        <select v-model="selectedBank" @change="clickBank" class="ml-auto bank-select custom-select">
          <option v-for="bank in banks" :key="bank">{{ bank }}</option>
        </select>
        <button @click="reset" class="custom-button">리셋</button>
      </div>
    </header>
    <hr class="my-3">

    <div v-if="dialog" class="dialog" @click.self="close">
      <div class="dialog-content">
        <div class="dialog-header">
          <h3>{{ selectedSaving?.['금융 상품명'] }}</h3>
          <div v-if="store.isLogin" class="dialog-buttons">
            <button v-if="isContractSaving" @click.prevent="deleteSavingUser" class="custom-button">가입 취소하기</button>
            <button v-else @click.prevent="addSavingUser" class="custom-button">가입하기</button>
          </div>
        </div>

        <table class="dialog-table">
          <tbody>
            <tr v-for="(value, key) in selectedSaving" :key="key" class="dialog-table-row">
              <td class="dialog-table-key">{{ key }}</td>
              <td class="dialog-table-value" v-if="key === '최고 한도'">
                {{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td class="dialog-table-value" v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto">
          <div v-if="savingType === 'F'">
            <BarChartDetailSaving :title="selectedSavingSimple.name + ' (자유적립형)'" :labels="selectedSaving.freedomLabels"
              :intr-rate="intrRateFreedom" :intr-rate2="intrRate2Freedom" saving-type="자유적립형" />
          </div>
          <div v-else-if="savingType === 'S'">
            <BarChartDetailSaving :title="selectedSavingSimple.name + ' (정기적금형)'" :labels="selectedSaving.regularLabels"
              :intr-rate="intrRateRegular" :intr-rate2="intrRate2Regular" saving-type="정기적금형" />
          </div>
          <div v-else-if="savingType === 'BOTH'">
            <BarChartDetailSaving :title="selectedSavingSimple.name + ' (자유적립형)'" :labels="selectedSaving.freedomLabels"
              :intr-rate="intrRateFreedom" :intr-rate2="intrRate2Freedom" saving-type="자유적립형" />
            <BarChartDetailSaving :title="selectedSavingSimple.name + ' (정기적금형)'" :labels="selectedSaving.regularLabels"
              :intr-rate="intrRateRegular" :intr-rate2="intrRate2Regular" saving-type="정기적금형" />
          </div>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="progress-circular"></div>
    </div>
    <table v-else-if="savingLength !== 0" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width"
            @click="sort(header.key)">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
          <td>{{ item['dcls_month'] }}</td>
          <td>{{ item['kor_co_nm'] }}</td>
          <td align="center">{{ item['name'] }}</td>
          <td align="center">{{ item['max_intr_rate2'] }}</td>
        </tr>
      </tbody>
    </table>

    <div v-else class="loading">
      <div class="progress-circular"></div>
    </div>
  </div>
</template>
        
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '../stores/counter'
import BarChartDetailSaving from '@/components/BarChartDetailSaving.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'name' },
  { title: '최고우대금리', align: 'end', width: '12%', key: 'max_intr_rate2' },
]

const make_data = function () {
  axios.get(`${store.DJANGO_URL}/financial/make_financial_data/`)
    .then((res) => {
      financialData.value = res.data || []
      console.log('받아온 데이터=', financialData.value)
    }).catch((err) => {
      console.log('에러가 발생했습니다. error=', err)
    })
}

const savings = ref([])
const savingLength = computed(() => savings.value.length)

const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedSavingSimple = ref(null)
const selectedSaving = ref(null)
const selectedSavingCode = computed(() => selectedSavingSimple.value?.['saving_code'])
const dialog = ref(false)
const loading = ref(false)
const sortKey = ref('')
const sortOrder = ref(1) // 1: ascending, -1: descending

const intrRateFreedom = ref([])
const intrRate2Freedom = ref([])
const intrRateRegular = ref([])
const intrRate2Regular = ref([])

const savingType = ref('NONE')

const isContractSaving = computed(() => {
  const userInfo = useCounterStore().userInfo;

  if (!userInfo) {
    console.error("userInfo is undefined");
    return false;
  }

  const contractSavingArray = Array.isArray(userInfo.savings) ? userInfo.savings : [];
  return contractSavingArray.some(e => e['fin_prdt_cd'] === selectedSavingCode.value);
});

const store = useCounterStore()
const router = useRouter()

const makeItems = function (item) {
  const result = {
    'saving_code': item['fin_prdt_cd'],
    'dcls_month': item['dcls_month'],
    'kor_co_nm': item['kor_co_nm'],
    'name': item['fin_prdt_nm'],
    'max_intr_rate2': Math.max(...item.options.map(opt => opt.intr_rate2 || 0)),  // 최고우대금리
    'saving_type': item.options.some(opt => opt.rsrv_type === 'S') ? (item.options.some(opt => opt.rsrv_type === 'F') ? 'BOTH' : 'S') : 'F'  // 상품 타입
  }

  return result
}
const getAllSavings = function () {
  loading.value = true
  axios.get(`${store.DJANGO_URL}/financial/saving_list/`)
    .then((res) => {
      const results = res.data
      savings.value = results.map(item => makeItems(item))
      banks.value = ['전체 보기', ...new Set(results.map(item => item.kor_co_nm))]
      loading.value = false
    })
    .catch((err) => {
      console.log(err)
      loading.value = false
    })
}

onMounted(async () => {
  await store.getUserInfo(store.userInfo.username);  // userInfo가 로드될 때까지 기다리기
  make_data();
  getAllSavings();
});
const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllSavings()
  } else {
    loading.value = true
    axios.get(`${store.DJANGO_URL}/financial/get_bank_saving/${selectedBank.value}/`)
      .then((res) => {
        savings.value = res.data.map(item => makeItems(item))
        loading.value = false
      })
      .catch((err) => {
        console.log(err)
        loading.value = false
      })
  }
}

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  selectedSavingSimple.value = data
  intrRateFreedom.value = []
  intrRate2Freedom.value = []
  intrRateRegular.value = []
  intrRate2Regular.value = []
  getSaving()
  dialog.value = true
}

const getSaving = async function () {
  if (!selectedSavingCode.value) {
    console.error('selectedSavingCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/`);
    const data = res.data;
    console.log("Saving data:", data);  // 데이터 확인용 콘솔 로그 추가

    const freedomOptions = data.options.filter(option => option.rsrv_type === 'F');
    const regularOptions = data.options.filter(option => option.rsrv_type === 'S');

    const freedomLabels = freedomOptions.map(option => `${option.save_trm}개월 금리`);
    const freedomRates = freedomOptions.map(option => option.intr_rate);
    const freedomRates2 = freedomOptions.map(option => option.intr_rate2);

    const regularLabels = regularOptions.map(option => `${option.save_trm}개월 금리`);
    const regularRates = regularOptions.map(option => option.intr_rate);
    const regularRates2 = regularOptions.map(option => option.intr_rate2);

    selectedSaving.value = {
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
      '기타 유의사항': data['etc_note'],
      'freedomLabels': freedomLabels.length ? freedomLabels : ['데이터 없음'],
      'freedomRates': freedomRates.length ? freedomRates : [0],
      'freedomRates2': freedomRates2.length ? freedomRates2 : [0],
      'regularLabels': regularLabels.length ? regularLabels : ['데이터 없음'],
      'regularRates': regularRates.length ? regularRates : [0],
      'regularRates2': regularRates2.length ? regularRates2 : [0]
    };

    intrRateFreedom.value = freedomRates.length ? freedomRates : [0];
    intrRate2Freedom.value = freedomRates2.length ? freedomRates2 : [0];
    intrRateRegular.value = regularRates.length ? regularRates : [0];
    intrRate2Regular.value = regularRates2.length ? regularRates2 : [0];

    if (freedomOptions.length && regularOptions.length) {
      savingType.value = 'BOTH'
    } else if (freedomOptions.length) {
      savingType.value = 'F'
    } else if (regularOptions.length) {
      savingType.value = 'S'
    } else {
      savingType.value = 'NONE'
    }

    console.log("freedomRates:", intrRateFreedom.value);
    console.log("freedomRates2:", intrRate2Freedom.value);
    console.log("regularRates:", intrRateRegular.value);
    console.log("regularRates2:", intrRate2Regular.value);
  } catch (err) {
    console.log(err);
  }
}

const addSavingUser = function () {
  axios.post(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, null, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
      const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
      if (answer) {
        router.push({ name: 'productManage', params: { username: store.userInfo.username } })
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteSavingUser = function () {
  axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedSavingCode.value}/contract/`, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getUserInfo(store.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
    })
}

const sort = function (key) {
  sortKey.value = key
  sortOrder.value *= -1

  savings.value.sort((a, b) => {
    if (a[key] < b[key]) return -1 * sortOrder.value
    if (a[key] > b[key]) return 1 * sortOrder.value
    return 0
  })
}

const reset = function () {
  selectedBank.value = '전체 보기'
  getAllSavings()
}
</script>
        
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
  font-family: 'NEXON Lv1 Gothic Low OTF';
}

.dialog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 70%;
  max-width: 90%;
  max-height: 70%;
  overflow-y: auto;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-buttons {
  display: flex;
  gap: 10px;
}

.dialog-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.dialog-table-row {
  border-bottom: 1px solid #ddd;
}

.dialog-table-key {
  padding: 8px;
  font-weight: bold;
  background-color: #f2f2f2;
  width: 30%;
}

.dialog-table-value {
  padding: 8px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

tbody>tr {
  transition: 200ms;
  cursor: pointer;
}

tbody>tr:hover {
  background-color: rgb(247, 250, 253);
  color: #1089FF;
}

.table {
  width: 90%;
  /* 테이블 너비를 90%로 줄임 */
  border-collapse: collapse;
  margin-top: 20px;
  margin-left: auto;
  /* 중앙 정렬을 위해 추가 */
  margin-right: auto;
  /* 중앙 정렬을 위해 추가 */
  font-family: 'NEXON Lv1 Gothic Low OTF';
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
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: bold;
}

.custom-button {
  background-color: #1089FF;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  font-family: 'NEXON Lv1 Gothic Low OTF';

}

.custom-button:hover {
  background-color: #0a73d9;
}

.custom-select {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: bold;
  color: #333;
}

.header-style h1 {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: bold;
  color: #333;
}

.search-container {
  display: flex;
  align-items: center;
}

.search-container select {
  margin-right: 10px;
}
</style>