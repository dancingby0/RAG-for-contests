<script setup lang="ts">
import {defineProps, ref, watch} from "vue";
import type {Communication} from "@/components/plain_objects/Communication";
import SendMessage from "@/components/icons/SendMessage.vue";
import Person from "@/assets/picture/person.jpg";
import Robot from "@/assets/picture/robot.png";


const props = defineProps<{
  chatList: Communication[];
  selectedChat: number;
  setSelectedChat:(id:number)=>void;
  sendMessage:(new_message:string)=>void;
}>();

const messageList = ref([]);
watch(props.chatList,(newValue,oldValue)=>{
  //messageList.value = newValue.find(chat=>);
})

const message = ref('');
// 一旦按下按钮,则设置当前信息,并清空输入框
const sendMessage = () => {
  if(message.value == ''){
    return;
  }
  props.sendMessage(message.value);
  message.value = '';
}

</script>

<template>
  <el-container v-if="selectedChat!=-1"
                style="display: flex;
                 justify-content: center;
                 align-items: center;
                 margin-right: 15rem;
">
    <el-header style="height: 40px; line-height: 40px; background-color: #f0f0f0; border-radius: 12px; margin-top: 1rem;">
      <div style=".d8ed659a {
    cursor: pointer;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: #262626;
    box-sizing: border-box;
    max-width: 100%;
    height: 40px;
    border-radius: 12px;
    padding: 8px 12px;
    font-size: 16px;
    font-weight: 600;
    line-height: 24px;
    overflow: hidden;
    max-width: 30rem;
}">
        {{ props.chatList.find(chat => chat.id == selectedChat)["title"] }}
      </div>
    </el-header>
    <el-main>
      <el-scrollbar max-height="50rem">
        <ul class="pop__clearfix" v-for="(message,index) in props.chatList.find(chat => chat.id == selectedChat).chatHistory" :key="index">
          <li class="pop__chat-msg-me2" v-if="message.id === 1">
              <el-avatar :src="Robot" style="width: 2rem;height: 2rem"></el-avatar>
            <div class="pop__chat-msg-content2">
              <div class="pop__chat-msg-msg2" v-if="message.cont"><span><div v-html="message.cont"></div></span></div>
            </div>
          </li>
          <li class="pop__chat-msg-me" v-if="message.id == 2">
            <div class="pop__chat-msg-content">
              <div class="pop__chat-msg-msg" v-if="message.cont"><span>{{ message.cont }}</span></div>
            </div>
            <el-avatar :src="Person" style="width: 2rem;height: 2rem ;flex-shrink: 0;"></el-avatar>
          </li>
        </ul>
      </el-scrollbar>
    </el-main>
    <el-footer>
      <el-input v-model="message" style="width: 30rem" placeholder="Please input"/>
      <el-button circle :icon="SendMessage" type="primary" style="margin-left: 10px" @click="sendMessage" />
    </el-footer>
  </el-container>

</template>

<style scoped>

.pop__chat-msg-content {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 3.5rem;
}

.pop__chat-msg-me {
  display: flex;
  margin-bottom: .72rem;
  margin-right: 2rem;
  float: right;
}

.pop__chat-msg-msg {
  background-color: rgb(179, 224, 156); /* 修正无效的小数点 */
  border-color: rgb(179, 224, 156);
  border-style: solid;
  border-width: 2px; /* 缩小边框 */
  border-radius: 0.5rem; /* 适当减少圆角 */
  color: #333;
  float: left;
  font-size: 1rem;
  margin: 0.5rem; /* 适当减少外边距 */
  padding: 0.5rem 0.8rem; /* 适当减少内边距 */
  max-width: 80%;
  position: relative;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-wrap: break-word;
}


.pop__clearfix {
  list-style: none;
  margin-left: 0rem;
  padding: 0;
}

.pop__clearfix:after {
  content: "";
  clear: both;
  display: block;
}

.pop__chat-msg-me2 {
  display: flex;
  margin-bottom: .36rem
}

.pop__chat-msg-content2 {
  width: 100%;
}

.pop__chat-msg-msg2 {
  background-color: #eeeef8;
  border-color: #eeeef8;
  border-style: solid;
  border-radius: .7rem;
  color: #333;
  float: left;
  font-size: 1rem;
  margin: 0.5rem; /* 适当减少外边距 */
  padding: 0.5rem 0.8rem; /* 适当减少内边距 */
  max-width: 80%;
  position: relative;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-wrap: break-word;
}

.content {
  background: #F2F2F2;
  padding: 0.2rem;
  overflow: scroll;
  box-sizing: border-box;
  padding-bottom: 0.8rem;
}

strong {
  font-weight: 600;
}
</style>