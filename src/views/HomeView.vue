<template>
  <Sidebar :chat-list="chatList" :delete-chat="deleteChat" :rename-chat="renameChat"
           :selected-chat="selectedChat" :set-selected-chat="setSelectedChat"
           :create-chat="createChat"
  />
  <RAGAnimation :stage="stage" :content="content" />
  <Chat :selected-chat="selectedChat" :chat-list="chatList" :set-selected-chat="setSelectedChat" :send-message="sendMessage" />
</template>

<script setup lang="ts">

import Sidebar from "@/components/Sidebar.vue";
import RAGAnimation from "@/components/RAGAnimation.vue";
import Chat from "@/components/Chat.vue";
import {onMounted, ref} from 'vue';

const stage = ref(1);
const content = ref<Array<string>>([]);
const chatList = ref([]);         // 存储用户的对话列表
const id_next = ref(0);
const selectedChat = ref(-1);     // 当前选中的对话
const message = ref('');          // 当前输入的消息
const sendMessage = (new_message:string) => {
  message.value = new_message;
  // 保存到对话列表
  chatList.value.find(chat => chat.id == selectedChat.value).chatHistory.push({id: 2, cont: message.value});
  localStorage.setItem('chatList', JSON.stringify(chatList.value));
  stage.value = 2;
  content.value = [message.value];
};

// 在页面加载时获取本地存储的对话列表
onMounted(() => {
  const savedChats = localStorage.getItem('chatList')
  let tmp = localStorage.getItem('id_next')
  id_next.value =  tmp == null ? 0 : JSON.parse(tmp)
  if (savedChats) {
    chatList.value = JSON.parse(savedChats);  // 从 localStorage 加载对话列表
  }
  if(!id_next.value){
    id_next.value = 0
  }
});

// 设置对话列表
const setChatList = (id:number,list:Array<any>) => {
  chatList.value.find(chat=>chat.id==id).chatHistory = list
};
// 重命名对话
const renameChat = (id:number,title:string) => {
  const chat = chatList.value.find(chat => chat.id === id);
  chat.title = title;
  // 更新时间
  chat.time = Date.now();
  localStorage.setItem('chatList', JSON.stringify(chatList.value));
};

// 删除对话
const deleteChat = (id:number) => {
  const index = chatList.value.findIndex(chat => chat.id === id);
  chatList.value.splice(index, 1);
  localStorage.setItem('chatList', JSON.stringify(chatList.value));
};

// 新建对话
const createChat = (title:string) => {
    const newChatData = {
      id: id_next.value,
      title: title,
      time: Date.now(),  // 获取当前时间(时间戳)
      chatHistory: [{id: 1, cont: "你好，我可以为你做些什么?"}]  // 初始化对话内容列表为空
    };
    id_next.value += 1;

    // 将新对话保存到列表
    chatList.value.push(newChatData);

    // 将对话列表保存到本地存储
    localStorage.setItem('chatList', JSON.stringify(chatList.value));

    // 将id_next保存到本地存储
    localStorage.setItem('id_next', JSON.stringify(id_next.value));
  };

// 设置selectedChat
const setSelectedChat = (id:number) => {
  selectedChat.value = id;
};

</script>

<style scoped>
</style>
