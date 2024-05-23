<!-- <template>
   <nav class="nav-links">
        
        <RouterLink class="nav-link" :to="{ name: 'DepositListView'}">예금 금리 비교</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'SavingListView'}">적금 금리 비교</RouterLink>
      </nav>
    
    <div>
        <RouterView/>
    </div>
</template>

<script setup>
 import { RouterLink,RouterView } from 'vue-router';
</script>
<style scoped>
.navbar {
  width: 100%;
  background-color: #fff;
  padding: 10px 20px;
  border-bottom: 1px solid #e0e0e0;
}

.navbar-content {
  display: flex;
  align-items: center;
}

.logo {
  width: 45px;
  height: 45px;
  margin-right: 10px;
}

.peek-title {
  font-family: Maplestory;
  font-size: 25px;
  font-weight: bold;
  color: #001e44;
  margin-right: auto;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  font-family: NEXONLv1GothicLowOTF;
  font-size: 16px;
  color: #001c43;
  text-decoration: none;
}

.nav-link:hover {
  text-decoration: underline;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logout-button {
  width: 125px;
  height: 40px;
  border-radius: 5px;
  background-color: #f5f5f5;
  border: none;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #e0e0e0;
}
</style> -->

<template>
  <div>
    <!-- 체크박스 형식 네비게이션 -->
    <div class="checkbox-navigation">
      <label>
        <input type="checkbox" v-model="isDepositChecked" @change="selectTab('deposit')" />
        예금 금리 비교
      </label>
      <label>
        <input type="checkbox" v-model="isSavingChecked" @change="selectTab('saving')" />
        적금 금리 비교
      </label>
    </div>

    <!-- 탭에 따라 컴포넌트를 동적으로 렌더링 -->
    <div>
      <component :is="currentTabComponent" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import DepositListView from '@/components/DepositListView.vue'; // 적절한 경로로 수정하세요
import SavingListView from '@/components/SavingListView.vue'; // 적절한 경로로 수정하세요

const currentTab = ref('deposit');
const isDepositChecked = ref(true);
const isSavingChecked = ref(false);

const selectTab = (tab) => {
  if (tab === 'deposit') {
    isDepositChecked.value = true;
    isSavingChecked.value = false;
    currentTab.value = 'deposit';
  } else {
    isDepositChecked.value = false;
    isSavingChecked.value = true;
    currentTab.value = 'saving';
  }
};

const currentTabComponent = computed(() => {
  return currentTab.value === 'deposit' ? DepositListView : SavingListView;
});
</script>

<style scoped>
.checkbox-navigation {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.checkbox-navigation label {
  font-family: NEXONLv1GothicLowOTF;
  font-size: 16px;
  color: #001c43;
}

.checkbox-navigation input {
  margin-right: 5px;
}
</style>

  