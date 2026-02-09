<template>
  <div class="chart-container">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const props = defineProps(['history']);

const chartData = computed(() => ({
  labels: props.history.map((_, i) => `День ${i + 1}`),
  datasets: [
    {
      label: 'История цены (₽)',
      backgroundColor: '#2481cc',
      borderColor: '#2481cc',
      data: props.history,
      tension: 0.3
    }
  ]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  }
};
</script>

<style scoped>
.chart-container {
  height: 200px;
  margin-top: 10px;
}
</style>
