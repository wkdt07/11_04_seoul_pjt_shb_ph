<script setup>
import { ref, watch } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Colors } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Colors)

const props = defineProps({
  selectedMonth: Object,
  labels: Array,
  intrRate: Array,
  intrRate2: Array
})

console.log('BarChart에서 intrRate:',props.intrRate)
console.log('BarChart에서 intrRate2:',props.intrRate2)

const chartData = ref({
  labels: props.labels,
  datasets: [
    {
      label: '평균 금리',
      data: [3.45, 4.08, 3.4, 3.35],
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
      text: `저축 금리 비교 (${props.selectedMonth.title})`
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

const chartRef = ref(null)

watch(
  () => [props.intrRate, props.intrRate2],
  ([newIntrRate, newIntrRate2]) => {
    if (chartRef.value) {
      chartData.value.datasets[1].data = newIntrRate
      chartData.value.datasets[2].data = newIntrRate2
      console.log('Updated chartData:', chartData.value)

      chartRef.value.chartInstance.update()
    }
  },
  { immediate: true }
)
</script>

<template>
  <div>
    <Bar
      ref="chartRef"
      class="mx-auto"
      style="width: 100%;"
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
