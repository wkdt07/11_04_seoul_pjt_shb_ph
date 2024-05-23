<template>
  <div class="chatbot-container">
    <div class="chat-header">
      <h2>AI 챗봇</h2>
      <button @click="toggleChat" class="toggle-chat-button">X</button>
    </div>
    <div class="chat-body">
      <div v-for="(message, index) in messages" :key="index" :class="{'user-message': message.user, 'bot-message': !message.user}">
        <p>{{ message.text }}</p>
      </div>
    </div>
    <form @submit.prevent="sendMessage" class="chat-input-container">
      <input type="text" v-model="inputMessage" placeholder="메시지를 입력하세요..." class="chat-input" />
      <button type="submit" class="send-button">전송</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const messages = ref([]);
const inputMessage = ref('');

const sendMessage = async () => {
  if (inputMessage.value.trim() === '') return;

  // 사용자 메시지 추가
  messages.value.push({ text: inputMessage.value, user: true });

  try {
    // Django 백엔드로 POST 요청 보내기
    const response = await fetch('http://127.0.0.1:8000/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}` // 사용자 인증 토큰이 필요할 경우 사용
      },
      body: JSON.stringify({ message: inputMessage.value })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();

    // 백엔드의 응답 메시지 추가
    messages.value.push({ text: data.message, user: false });
  } catch (error) {
    console.error('Error:', error);
    messages.value.push({ text: '에러가 발생했습니다.', user: false });
  }

  // 입력 필드 초기화
  inputMessage.value = '';
};

const toggleChat = () => {
  const chatContainer = document.querySelector('.chatbot-container');
  chatContainer.classList.toggle('hidden');
};
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low';
  src: url('@/assets/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.chatbot-container {
  position: fixed;
  bottom: 0;
  right: 20px;
  width: 350px;
  max-height: 70%;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  font-family: 'NEXON Lv1 Gothic Low', sans-serif;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #1089FF;
  color: white;
  font-size: 18px;
}

.toggle-chat-button {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.chat-body {
  padding: 10px;
  overflow-y: auto;
  max-height: 400px;
}

.user-message {
  text-align: right;
  background-color: #e1f7d5;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.bot-message {
  text-align: left;
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.chat-input-container {
  display: flex;
  padding: 10px;
  background-color: #f0f2f5;
}

.chat-input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  margin-right: 10px;
  box-sizing: border-box;
}

.send-button {
  padding: 10px 20px;
  background-color: #1089FF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.send-button:hover {
  background-color: #0a73d9;
}

.hidden {
  display: none;
}
</style>
