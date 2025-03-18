<script setup lang="ts">
import {defineProps, onMounted, reactive, watch} from 'vue'
import {ref} from "vue";
import {ElMessageBox, ElMessage} from "element-plus";
import type {Communication} from "@/components/plain_objects/Communication";
import MessageMore from "@/components/icons/MessageMore.vue";

const props = defineProps<{
  chatList: Communication[];
  renameChat: (id: number, title: string) => void;
  deleteChat: (id: number) => void;
  selectedChat: number;
  setSelectedChat: (id: number) => void;

}>();

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

const clarifyCommunications = (chatList: Communication[]) => {
  // 清空各个数组
  todayCommunications.value = []
  yesterdayCommunications.value = []
  lastSevenDaysCommunications.value = []
  lastOneMonthCommunications.value = []
  lastThreeMonthsCommunications.value = []
  longLongAgoCommunications.value = []


  for (let i = 0; i < chatList.length; i++) {
    if (chatList[i].time > oneDayAgo) {
      todayCommunications.value.push(chatList[i])
    } else if (chatList[i].time > twoDaysAgo) {
      yesterdayCommunications.value.push(chatList[i])
    } else if (chatList[i].time > sevenDaysAgo) {
      lastSevenDaysCommunications.value.push(chatList[i])
    } else if (chatList[i].time > oneMonthAgo) {
      lastOneMonthCommunications.value.push(chatList[i])
    } else if (chatList[i].time > threeMonthsAgo) {
      lastThreeMonthsCommunications.value.push(chatList[i])
    } else {
      longLongAgoCommunications.value.push(chatList[i])
    }
  }

  {
    console.log("输出总对话")
    console.log(chatList)
    console.log(chatList.length)
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
  clarifyCommunications(props.chatList)
})

watch(() => props.chatList, (newValue) => {
  console.log("watch, 数组更新了")
  clarifyCommunications(newValue)
}, {deep: true})

const handleCommunicationClick = (index: number) => {
  props.setSelectedChat(index);
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

const mouseAt = ref(-1);

const smallBtnMoreVisible=ref(-1)

const renameChat = (id:number) => {
  ElMessageBox.prompt('请输入新的名称', 'Tip', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    inputPattern:
        /\S+.*/,
    inputErrorMessage: '输入不能为空!',
    // 默认填入原来的名称
    inputValue: props.chatList.find((communication) => communication.id == id)?.title
  })
      .then(({ value }) => {
        props.renameChat(id, value)
        ElMessage({
          type: 'success',
          message: '重命名成功',
        });
      })
      .catch(() => {
        ElMessage({
          type: 'info',
          message: '已取消重命名',
        })
      })
}

const deleteChat = (id:number) => {
  ElMessageBox.confirm('此操作将永久删除该对话, 是否继续?', 'Tip', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        props.deleteChat(id)
        ElMessage({
          type: 'success',
          message: '删除成功!',
        });
      })
      .catch(() => {
        ElMessage({
          type: 'info',
          message: '已取消删除'
        });
      });
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


        <div v-for="communication in communicationTitleDict.communication.value"
        @mouseenter="mouseAt=communication.id"
        @mouseleave="mouseAt=-1">

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
  text-align: left;
"
          >
            <template #default>
              <div
                  class="popover-content"
                  @mouseenter="()=>{hidePopover(communication.id);}"
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
                    class="communication-option"fffffffcb vvnjvvvvbvvnjxgmdvvvvvvvvvxmgddddddddddvvvvxndsgjjjjjjjsdsgjmvff vcbndxsjgrmhhv
                    :class="{'communication-pressed': selectedChat == communication.id,
                    'communication-hovered': bigBtnHover == communication.id&& selectedChat!=communication.id}"
                    @click="handleCommunicationClick(communication.id)"
                    @mouseenter="()=>{delayedShowPopover(communication.id)}"
                    @mouseleave="()=>{hidePopover(communication.id)}"
                >
                  <div class="btn-content">
                    <span class="text-mask">{{ communication.title }}</span>
                  </div>
                </el-button>
                <el-popover :width="140" trigger="click"  :teleported="false"  >
                  <div style="text-align: right; margin: 0">
                    <el-button size="small" @click="renameChat(communication.id)">
                      重命名
                    </el-button>
                    <el-button size="small" type="danger" @click="deleteChat(communication.id)">
                      删除
                    </el-button>
                  </div>
                  <template #reference>
                    <el-button
                        :icon="MessageMore"
                        plain
                        round
                        text
                        class="small-btn"
                        v-show="mouseAt == communication.id"
                        @mouseenter="()=>{hidePopover(communication.id);showBigBtnHover(communication.id);}"
                        @mouseleave="()=>{hideBigBtnHover();}"
                        @click="smallBtnMoreVisible = communication.id"
                    ></el-button>
                  </template>
                </el-popover>


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