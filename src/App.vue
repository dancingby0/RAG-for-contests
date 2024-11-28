<template>
  <div id="app">
    <h1>Vue 3 Frontend to Backend Example</h1>

    <div>
      <textarea v-model="content" rows="4" cols="50" placeholder="Enter some content..."></textarea>
    </div>
    
    <button @click="sendContent">Send Content</button>
    
    <div v-if="response">
      <h2>Response from Backend:</h2>
      <p>{{ response }}</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'App',
  setup() {
    // 定义响应式数据
    const content = ref('');
    const response = ref('');

    // 发送内容到后端
    const sendContent = async () => {
      try {
        const res = await axios.post('http://localhost:8000/api/send', { content: content.value });
        response.value = res.data.message; // 获取后端返回的内容
      } catch (error) {
        console.error("Error:", error);
        response.value = "An error occurred while sending content to the backend.";
      }
    };

    return {
      content,
      response,
      sendContent
    };
  }
};
</script>

<style scoped>
textarea {
  margin-bottom: 10px;
}
button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #367a46;
}
</style>
