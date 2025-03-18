<script setup lang="ts">
import {onMounted, onUnmounted, ref, watch,defineProps} from "vue";
import {SERVER_URL} from "@/constants/constants";
import AnimationSVG from "@/components/icons/AnimationSVG.vue";

const props = defineProps<{
  stage: number;
  content: Array<any>;
  setStage: (new_stage: number) => void;
  setContent: (new_content: Array<string>) => void;
  triggerStage8: () => void;
}>()

let socket = new WebSocket(SERVER_URL + '/api/ws/animation');
onMounted(() => {
  socket.onopen = () => {
    console.log('WebSocket connected');
  };
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    props.setStage(data.stage);
    props.setContent(data.content);
  };
  socket.onclose = () => {
    console.log('WebSocket closed');
  };
  socket.addEventListener('open', function (event) {
    socket.send('Animation connected');
  });

  // 接受到消息后,设置stage和content
  socket.addEventListener('message', function (event) {
    const data = JSON.parse(event.data);
    props.setStage(data.stage);
    props.setContent(data.content);
  });
});

onUnmounted(() => {
  socket.close();
});

const showAnimation = ref(false);
// showAnimation发生变化时,向SERVER_URL/api/showAnimation发送post请求,传递showAnimation的值
watch(showAnimation, (newValue, oldValue) => {
  fetch(SERVER_URL + '/api/showAnimation', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      showAnimation: newValue
    })

  })
  console.log(JSON.stringify({
    showAnimation: newValue
  }))
})
</script>

<template>
  <div style="margin-left: 3rem">
    <br />
    <br />
    <br />
    <span style="white-space: nowrap"> 动画展示 </span>
    <el-switch
        style="position:relative;z-index : 1000;"
        v-model="showAnimation"
    />
  </div>
<!--  转移时间-->
  <div v-if="showAnimation" style="display: flex;align-items: center;
  transform: scale(0.8);justify-content: left;margin-left: -10rem;
">
    <AnimationSVG :content="content" :stage="stage" ></AnimationSVG>
  </div>

</template>

<style scoped>

</style>