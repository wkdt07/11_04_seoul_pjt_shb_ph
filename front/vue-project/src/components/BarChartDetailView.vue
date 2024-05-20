<script setup>
import { ref, watch, defineProps, nextTick, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  title: String,
  averageIntrRate: Array,
  intrRate: Array,
  intrRate2: Array
})

console.log('BarChartDetail에서 intrRate', props.intrRate)
console.log('BarChartDetail에서 intrRate2', props.intrRate2)

const chartRef = ref(null)

const chartData = ref({
  labels: ['6개월 금리', '12개월 금리', '24개월 금리', '36개월 금리'],
  datasets: [
    {
      label: '평균 금리',
      data: props.averageIntrRate,
      backgroundColor: 'grey',
      stack: 'Stack 0'
    },
    {
      label: '저축 금리',
      data: props.intrRate,
      backgroundColor: '#1089FF',
      stack: 'Stack 1'
    },
    {
      label: '최고 우대 금리',
      data: props.intrRate2,
      backgroundColor: 'red',
      stack: 'Stack 2'
    },
  ]
})

const chartOptions = ref({
  plugins: {
    title: {
      display: true,
      text: `<${props.title}> 상품의 저축 금리`
    },
  },
  responsive: true,
  scales: {
    x: {
      stacked: true,
      ticks: {
        maxRotation: 0,
        minRotation: 0,
        font: {
          size: 10
        }
      }
    },
  },
})

const updateChartData = () => {
  console.log('Updating chart data 함수', props.intrRate, props.intrRate2)
  chartData.value.datasets[0].data = [...props.averageIntrRate]
  chartData.value.datasets[1].data = [...props.intrRate]
  chartData.value.datasets[2].data = [...props.intrRate2]

  nextTick(() => {
    if (chartRef.value && chartRef.value.chartInstance) {
      chartRef.value.chartInstance.update()
    }
  })
}

watch(
  () => [props.averageIntrRate, props.intrRate, props.intrRate2],
  ([newAverageIntrRate, newIntrRate, newIntrRate2]) => {
    console.log('Props changed', newAverageIntrRate, newIntrRate, newIntrRate2)
    updateChartData()
  },
  { immediate: true, deep: true }
)

onMounted(() => {
  updateChartData()
})
</script>

<template>
  <div>
    <Bar
      ref="chartRef"
      class="mx-auto"
      :style="{ width: '100%' }"
      :options="chartOptions"
      :data="chartData"
    />
  </div>
</template>

<style scoped>
.mx-auto {
  margin: auto;
}
</style>
