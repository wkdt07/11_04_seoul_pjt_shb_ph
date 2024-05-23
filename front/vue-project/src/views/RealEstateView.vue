<template>
  <div>
    <ul>
      <li v-for="realEstate in realEstates" :key="realEstate.id">
        {{ realEstate.date_time }} - {{ realEstate.price }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useCounterStore } from '../stores/counter';

const realEstates = ref([]);
const store = useCounterStore();

const makeData = async () => {
  try {
    console.log('Making data...');
    const response = await axios.get(`${store.DJANGO_URL}/real_estate/make_data/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    console.log('Data made:', response.data);
  } catch (error) {
    console.error('Error making data:', error);
  }
};

const fetchRealEstates = async () => {
  try {
    console.log('Fetching real estate data...');
    console.log('Token:', store.token);

    const response = await axios.get(`${store.DJANGO_URL}/real_estate/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });

    console.log('Response data:', response.data);
    realEstates.value = response.data;
    console.log('Real estates:', realEstates.value);
  } catch (error) {
    console.error('Error fetching real estate data:', error);
  }
};

onMounted(async () => {
  await makeData();
  await fetchRealEstates();
});
</script>
