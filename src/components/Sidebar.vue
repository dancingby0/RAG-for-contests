<template>
  <div>
    <!-- 折叠按钮, 可以随着折叠栏移动 -->

    <el-tooltip
        effect="dark"
        placement="bottom"
        :content="isCollapsed ? '展开侧边栏':'收起侧边栏'"
        show-after="500"
    >
      <el-button
          @click="toggleSidebar"
          plain
          class="collapse-btn"
          :style="[collapseButtonStyles,isCollapsed ? { position: 'absolute', top: '20px', left: '10px' } : {}]"
          :icon="SidebarButton"
          size="large"
          text
      >
      </el-button>
    </el-tooltip>

    <!-- 可折叠的侧边栏 -->
    <div :class="['sidebar', { 'collapsed': isCollapsed }]">
      <div class="sidebar-item">
        <!--        这里设计容器: 顶部和中部 -->
        <!--            这里放标题-->
        <div class="sidebar-header">
          <h2>露娜赛高队</h2>
        </div>
        <!--            这里放主要内容: 创建新会话按钮,会话内容-->
        <el-space fill="fill" wrap>
          <div class="sidebar-content">
            <el-button
                type="primary"
                size="large"
                text
                round
                :icon="NewMessage"
                class="new-message-button"
                @click="newDialogVisible=true"
            >
              创建新会话
            </el-button>
            <el-dialog
                v-model="newDialogVisible"
                title="创建新会话"
                width="40rem"
            >
              <!-- 表单 -->
              <el-form :model="newChat">
                <el-form-item label="对话标题" :label-width="formLabelWidth">
                  <el-input v-model="newChat.title" placeholder="请输入对话标题"/>
                </el-form-item>
              </el-form>
              <template #footer>
                <span class="dialog-footer">
        <el-button @click="newDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createNewChat">确定</el-button>
      </span>
              </template>

            </el-dialog>

            <CommunicationList :chat-list="props.chatList" :renameChat="props.renameChat" :deleteChat="props.deleteChat"
            :selected-chat="props.selectedChat" :set-selected-chat="props.setSelectedChat"
            />

          </div>
        </el-space>
      </div>
    </div>
  </div>
</template>



<script setup lang="ts">
import { ref,defineProps} from 'vue';
import SidebarButton from "@/components/icons/SidebarButton.vue";
import NewMessage from "@/components/icons/NewMessage.vue";
import CommunicationList from "@/components/CommunicationList.vue";
import type {Communication} from "@/components/plain_objects/Communication";

// 控制侧边栏折叠状态
const isCollapsed = ref(false);

const props = defineProps<{
  chatList: Communication[];
  selectedChat: number;
  setSelectedChat: (id: number) => void;
  createChat: (title: string) => void;
  renameChat: (id: number, title: string) => void;
  deleteChat: (id: number) => void;
}>()

// 切换折叠状态
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};

// 处理对话框
const newDialogVisible = ref(false);

// 组件状态
const formLabelWidth = '80px';     // 表单标签宽度
const newChat = ref({title: ''}); // 新建对话的表单数据

// 重置新建对话表单
const resetDialog = () => {
  newChat.value.title = '';  // 清空表单
};


// 新建对话
const createNewChat = () => {
  if (newChat.value.title) {
    console.log("创建新的对话")
    props.createChat(newChat.value.title);

    // 关闭弹窗并重置表单
    newDialogVisible.value = false;
    resetDialog();
  } else {
    alert('请输入对话标题');
  }
};

// style

const collapseButtonStyles = {
  width: "40px",
  height: "40px",
  fontSize: "28px"
}
</script>





<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #f9fbff;
  transition: width 0.3s ease;
  position: relative;
}

.sidebar.collapsed {
  width: 0; /* 折叠后的宽度 */
}

.sidebar-header {
  padding: 20px;
  color: #000000;
  text-align: center;
}

.el-menu {
  padding: 0;
}

.el-menu-item {
  color: white;
  white-space: nowrap; /* 禁止换行 */
  overflow: hidden;
}

.el-menu-item .menu-text {
  display: inline-block;
  vertical-align: middle;
  white-space: nowrap; /* 禁止换行 */
  overflow: hidden;
}

.el-menu-item i {
  margin-right: 10px;
}


.collapse-btn {
  position: absolute;
  top: 20px;
  left: 250px; /* 让按钮定位到右侧 */
  transition: left 0.3s ease;
}

.sidebar.collapsed .collapse-btn {
  left: 10px; /* 折叠时将按钮移动到侧边栏内 */
}

.sidebar-item {
  white-space: nowrap;
  overflow: hidden;
}

.new-message-button {
  width: 8rem;
  height: 3.5rem;
  font-size: 1rem;
  color: #4d6bfe;
  background-color: rgb(223 237 255);
  --el-bg-color: #c6dcf8;
}

.sidebar-content {
  margin-left: 15px;

}


</style>
