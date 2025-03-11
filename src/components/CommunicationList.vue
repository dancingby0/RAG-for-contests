<script setup lang="ts">
import {defineProps, onMounted, reactive, watch} from 'vue'
import {ref} from "vue";
import type {Communication} from "@/components/plain_objects/Communication";
import MessageMore from "@/components/icons/MessageMore.vue";

const props = defineProps<{
  communicationList: Communication[];
}>();

// 存取目前选中的对话(-1表示没有选中)
const selectedCommunicationIndex = ref(-1)

const todayCommunications = ref<Communication[]>([])
const yesterdayCommunications = ref<Communication[]>([])
const lastSevenDaysCommunications = ref<Communication[]>([])
const lastOneMonthCommunications = ref<Communication[]>([])
const lastThreeMonthsCommunications = ref<Communication[]>([])
const longLongAgoCommunications = ref<Communication[]>([])
const now = Date.now(); // 单位: 毫秒
const oneDayAgo = now - 24 * 60 * 60 * 1000;
const twoDaysAgo = now - 2 * 24 * 60 * 60 * 1000;
const sevenDaysAgo = now - 7 * 24 * 60 * 60 * 1000;
const oneMonthAgo = now - 30 * 24 * 60 * 60 * 1000;
const threeMonthsAgo = now - 90 * 24 * 60 * 60 * 1000;

const clarifyCommunications = (communicationList: Communication[]) => {
  // 清空各个数组
  todayCommunications.value = []
  yesterdayCommunications.value = []
  lastSevenDaysCommunications.value = []
  lastOneMonthCommunications.value = []
  lastThreeMonthsCommunications.value = []
  longLongAgoCommunications.value = []


  for (let i = 0; i < communicationList.length; i++) {
    if (communicationList[i].time > oneDayAgo) {
      todayCommunications.value.push(communicationList[i])
    } else if (communicationList[i].time > twoDaysAgo) {
      yesterdayCommunications.value.push(communicationList[i])
    } else if (communicationList[i].time > sevenDaysAgo) {
      lastSevenDaysCommunications.value.push(communicationList[i])
    } else if (communicationList[i].time > oneMonthAgo) {
      lastOneMonthCommunications.value.push(communicationList[i])
    } else if (communicationList[i].time > threeMonthsAgo) {
      lastThreeMonthsCommunications.value.push(communicationList[i])
    } else {
      longLongAgoCommunications.value.push(communicationList[i])
    }
  }

  {
    console.log("输出总对话")
    console.log(communicationList)
    console.log(communicationList.length)
    console.log("输出今天的对话")
    console.log(todayCommunications.value)
    console.log(todayCommunications.value.length)
    console.log("输出昨天的对话")
    console.log(yesterdayCommunications.value)
    console.log(yesterdayCommunications.value.length)
    console.log("输出最近七天的对话")
    console.log(lastSevenDaysCommunications.value)
    console.log(lastSevenDaysCommunications.value.length)
    console.log("输出最近一个月的对话")
    console.log(lastOneMonthCommunications.value)
    console.log(lastOneMonthCommunications.value.length)
    console.log("输出最近三个月的对话")
    console.log(lastThreeMonthsCommunications.value)
    console.log(lastThreeMonthsCommunications.value.length)
    console.log("输出很久以前的对话")
    console.log(longLongAgoCommunications.value)
    console.log(longLongAgoCommunications.value.length)
  }

}

onMounted(() => {
  clarifyCommunications(props.communicationList)
})

watch(() => props.communicationList, (newValue) => {
  console.log("watch, 数组更新了")
  clarifyCommunications(newValue)
}, {deep: true})

const selectedCommunication = ref(-1)

const handleCommunicationClick = (index: number) => {
  selectedCommunication.value = index
}
const CommunicationTitleDictList = [
  {"title": "今天", "communication": todayCommunications},
  {"title": "昨天", "communication": yesterdayCommunications},
  {"title": "近七天", "communication": lastSevenDaysCommunications},
  {"title": "近一个月", "communication": lastOneMonthCommunications},
  {"title": "近三个月", "communication": lastThreeMonthsCommunications},
  {"title": "很久以前", "communication": longLongAgoCommunications}
]

const popoverVisible = ref(-1);
let popoverTimeout:number = 0;

const delayedShowPopover = (id:number) => {
  popoverTimeout = setTimeout(() => {
    popoverVisible.value= id;
  }, 500);
};

// 立即隐藏 popover
const hidePopover = (id:number) => {
  clearTimeout(popoverTimeout);
  popoverVisible.value = -1;
};

const smallBtnShow = ref(-1);

const showSmallBtn = (id:number) => {
  smallBtnShow.value = id;
}
const hideSmallBtn = () => {
  smallBtnShow.value = -1;
}

const bigBtnHover = ref(-1);

const showBigBtnHover = (id:number) => {
  bigBtnHover.value = id;
}

const hideBigBtnHover = () => {
  bigBtnHover.value = -1;
}

</script>

<template>
  <div>
    <br/>
    <br/>
    <el-scrollbar max-height="40rem" class="custom-scrollbar">
      <!--    如果时间有今天的话,显示  -->
      <div v-for="communicationTitleDict in CommunicationTitleDictList">
        <el-text v-if="communicationTitleDict.communication.value.length != 0" tag="b" style="color: #555;"
                 class="title-text">{{ communicationTitleDict.title }}
        </el-text>


        <div v-for="communication in communicationTitleDict.communication.value">

          <el-popover
              ref="popoverRef"
              :visible="popoverVisible == communication.id"
              placement="top"
              trigger="hover"
              :width="null"
              show-after="500"
              popper-style="
  max-width: 12rem ;
  min-width: 1rem ;
  white-space: normal;
  word-wrap: break-word;
  text-align: left; "
          >
            <template #default>
              <div
                  class="popover-content"
                  @mouseenter="hidePopover(communication.id)"
              >
                {{ communication.title }}
              </div>
            </template>
            <template #reference>
              <div style="display: flex">
                <el-button
                    text
                    plain
                    round
                    class="communication-option"
                    :class="{'communication-pressed': selectedCommunication == communication.id,
                    'communication-hovered': bigBtnHover == communication.id}"
                    @click="handleCommunicationClick(communication.id)"
                    @mouseenter="()=>{delayedShowPopover(communication.id);}"
                    @mouseleave="()=>{hidePopover(communication.id);}"
                >
                  <div class="btn-content">
                    <span class="text-mask">{{ communication.title }}</span>
                  </div>
                </el-button>
                <el-button
                    :icon="MessageMore"
                    plain
                    round
                    text
                    class="small-btn"
                    @mouseenter="hidePopover(communication.id)"
                ></el-button>
              </div>

            </template>
          </el-popover>

        </div>
        <br/>
      </div>
    </el-scrollbar>
  </div>
</template>

<style scoped>

.communication-option {
  height: 35px;
  width: 13.5rem;
  white-space: nowrap;
  overflow: hidden;
  transition: background-color 0.3s, color 0.3s;
  cursor: pointer;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  padding-left: 15px;
  text-align: left;
  font-size: 15px;
  border-radius: 10px !important; /* 这里调整圆角大小 */
}

/* 鼠标悬停时 */
.communication-option:hover {
  background-color: rgb(235.9, 245.3, 255) !important;
}

.communication-pressed {
  background-color: rgb(219 234 254) !important;
}

.communication-pressed:hover {
  background-color: rgb(219 234 254) !important;
}

.communication-hovered{
  background-color: rgb(235.9, 245.3, 255) !important;
}

.text-mask {
  display: block;
  width: 165px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: clip;

  /* 使用 mask-image 让右侧文字渐隐 */
  /* 渐隐效果从 100px 开始 */
  -webkit-mask-image: linear-gradient(to right,
  rgba(0, 0, 0, 1) 0px,
  rgba(0, 0, 0, 1) 140px,
  rgba(0, 0, 0, 0) 160px
  );
  mask-image: linear-gradient(to right,
  rgba(0, 0, 0, 1) 0px,
  rgba(0, 0, 0, 1) 140px,
  rgba(0, 0, 0, 0) 160px
  );
}

.title-text {
  color: #555;
  display: block; /* 让其独占一行 */
  text-align: left; /* 确保文字靠左 */
  margin: 10px 0; /* 上下各占 20px 空白 */
}

.custom-scrollbar {
  position: relative;
  width: 225px;
}

:deep(.el-scrollbar__bar.is-vertical) {
  right: 0px !important;
}

.small-btn {
  position: absolute;
  right: 12px;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.btn-content {
  display: flex;
  align-items: center;
  margin-block: 2px;
}

.small-btn:hover {
  background-color: #f9fbff !important;

}
</style>