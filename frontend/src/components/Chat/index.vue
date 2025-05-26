<template>
  <div class="chat-page">
    <!-- sidebar 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
      <!-- sidebar-header 侧边栏头部 -->
      <div class="sidebar-header">
        <h2 v-show="!isSidebarCollapsed">Mindo</h2>
        <el-button
          class="collapse-btn"
          @click="toggleSidebar"
          :icon="isSidebarCollapsed ? Expand : Fold"
          circle
        />
      </div>

      <!-- sidebar-content 侧边栏主体内容部分 -->
      <div class="sidebar-content">
        <!-- new-chat-btn 创建新聊天按钮 -->
        <div class="new-chat-btn">
          <el-tooltip
            v-if="isSidebarCollapsed"
            content="新聊天"
            placement="right"
          >
            <el-button
              type="primary"
              @click="handleNewChat"
              :icon="Plus"
              circle
            />
          </el-tooltip>
          <el-button v-else type="primary" @click="handleNewChat" :icon="Plus">
            新聊天
          </el-button>
        </div>

        <!-- 聊天历史列表 -->
        <div class="chat-history" v-show="!isSidebarCollapsed">
          <el-scrollbar height="calc(100vh - 180px)">
            <el-menu :default-active="activeChat" @select="handleSelectChat">
              <el-menu-item
                v-for="chat in chats"
                :key="chat.id"
                :index="chat.id"
              >
                <template #title>
                  <span>{{ chat.title }}</span>
                  <div class="chat-actions">
                    <el-popover
                      placement="right"
                      :width="200"
                      trigger="click"
                      v.model:visible="titlePopoverVisible[chat.id]"
                    >
                      <template #reference>
                        <el-button
                          type="text"
                          :icon="Edit"
                          @click.stop="handleEditTitle(chat.id)"
                          class="edit-btn"
                        />
                      </template>
                      <el-input
                        v-model="editingTitle"
                        placeholder="输入新标题"
                        @keyup.enter="confirmEditTitle"
                        :ref="(el) => setTitleInputRef(chat.id, el)"
                      />
                      <div style="text-align: right; margin-top: 10px">
                        <el-button
                          size="small"
                          @click="cancelEditTitle(chat.id)"
                          >取消</el-button
                        >
                        <el-button
                          size="small"
                          type="primary"
                          @click="confirmEditTitle"
                          >确定</el-button
                        >
                      </div>
                    </el-popover>
                    <el-button
                      type="text"
                      :icon="Delete"
                      @click.stop="deleteChat(chat.id)"
                      class="delete-btn"
                    />
                  </div>
                </template>
              </el-menu-item>
            </el-menu>
          </el-scrollbar>
        </div>
      </div>

      <!-- sidebar-footer 底部用户区域 -->
      <div class="sidebar-footer">
        <el-tooltip
          v-if="isSidebarCollapsed"
          content="登录/注册"
          placement="right"
        >
          <el-button @click="handleLogin" :icon="User" circle />
        </el-tooltip>
        <el-button v-else @click="handleLogin" :icon="User">去登录</el-button>
      </div>
    </aside>

    <!-- main-content 主内容区 -->
    <main class="main-content" :class="{ collapsed: isSidebarCollapsed }">
      <div class="chat-container">
        <!-- chat-header 聊天头部 -->
        <div class="chat-header">
          <el-input
            v-if="isEditingMainTitle"
            v-model="currentChatTitleEdit"
            @blur="saveMainTitle"
            @keyup.enter="saveMainTitle"
            size="large"
            class="title-input"
            ref="mainTitleInput"
          />
          <h3 v-else @click="startEditingMainTitle" class="chat-title">
            {{ currentChatTitle || "新聊天" }}
          </h3>
        </div>

        <!-- 聊天消息区域 -->
        <div class="chat-messages">
          <el-scrollbar ref="messagesScrollbar">
            <!-- 欢迎页面 -->
            <div v-if="showWelcomeScreen" class="welcome-screen">
              <div class="welcome-content">
                <div class="welcome-header">
                  <h3>我是 DeepSeek，很高兴见到你！</h3>
                  <p>我可以帮你呵护你，这次我、写作者的创意内容，请把你的任务交给同学。</p>
                </div>
                
                <!-- 中间的输入框 -->
                <div class="chat-input">
                  <div class="input-container middle">
                    <el-input
                      v-model="newMessage"
                      type="textarea"
                      :rows="2"
                      :autosize="{ minRows: 2, maxRows: 8 }"
                      placeholder="输入消息..."
                      resize="none"
                      @keyup.enter="handleSendMessage"
                      class="message-input"
                    />
                    <div class="input-footer">
                      <div class="input-actions-left">
                        <el-button type="text" :icon="MagicStick" class="action-btn round">
                          深度思考 (R1)
                        </el-button>
                        <el-button type="text" :icon="Connection" class="action-btn round">
                          联网搜索
                        </el-button>
                      </div>
                      <div class="input-actions-right">
                        <el-button type="text" :icon="Upload" class="action-btn" />
                        <el-button 
                          type="primary" 
                          :icon="Promotion" 
                          @click="handleSendMessage"
                          :disabled="!newMessage.trim()"
                          class="send-btn"
                          circle
                        />
                      </div>
                    </div>
                    <div class="ai-tip">内容由 AI 生成，请仔细甄别</div>
                  </div>
                </div> 
              </div>
            </div>

            <div
              v-for="message in currentMessages"
              :key="message.id"
              class="message"
              :class="{
                user: message.sender === 'user',
                ai: message.sender === 'ai',
              }"
            >
              <div class="avatar">
                <el-avatar :icon="message.sender === 'user' ? User : ChatLineRound" />
              </div>
              <div class="message-content">
                <div class="text">{{ message.text }}</div>
                <div class="message-time">{{ formatTime(message.time) }}</div>
              </div>
            </div>
          </el-scrollbar>
        </div>

        <!-- 聊天输入区域 -->
        <div class="chat-input" v-if="!showWelcomeScreen">
          <div class="input-container">
            <el-input
              v-model="newMessage"
              type="textarea"
              :rows="2"
              :autosize="{ minRows: 2, maxRows: 8 }"
              placeholder="输入消息..."
              resize="none"
              @keyup.enter="handleSendMessage"
              class="message-input"
            />
            <div class="input-footer">
              <div class="input-actions-left">
                <el-button type="text" :icon="MagicStick" class="action-btn round">
                  深度思考 (R1)
                </el-button>
                <el-button type="text" :icon="Connection" class="action-btn round">
                  联网搜索
                </el-button>
              </div>
              <div class="input-actions-right">
                <el-button type="text" :icon="Upload" class="action-btn" />
                <el-button 
                  type="primary" 
                  :icon="Promotion" 
                  @click="handleSendMessage"
                  :disabled="!newMessage.trim()"
                  class="send-btn"
                  circle
                />
              </div>
            </div>
            <div class="ai-tip">内容由 AI 生成，请仔细甄别</div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import {
  Fold,
  Expand,
  Plus,
  User,
  Delete,
  Promotion,
  Edit,
  MagicStick,
  Connection,
  Upload,
} from "@element-plus/icons-vue";

const showWelcomeScreen = ref(true); // 控制欢迎页面显示
const isSidebarCollapsed = ref(true); // 侧边栏默认收起

const chats = ref([
  {
    id: "1",
    title: "示例对话",
    messages: [
      {
        id: 1,
        sender: "ai",
        text: "你好！我是AI助手，有什么可以帮您的吗？",
        time: new Date(Date.now() - 60000),
      },
    ],
  },
]);

const activeChat = ref("1");
const newMessage = ref("");
const messagesScrollbar = ref(null);
const editingTitle = ref("");
const editingChatId = ref(null);
const titlePopoverVisible = ref({});
const titleInputRefs = ref({});
const isEditingMainTitle = ref(false);
const currentChatTitleEdit = ref("");
const mainTitleInput = ref(null);

// 计算属性
// 获取当前对话内容的标题
const currentChatTitle = computed(() => {
  const chat = chats.value.find((c) => c.id === activeChat.value);
  return chat ? chat.title : "";
});
// 获取当前对话内容
const currentMessages = computed(() => {
  const chat = chats.value.find((c) => c.id === activeChat.value);
  return chat ? chat.messages : [];
});


//  handleNewChat 创建新聊天
const handleNewChat = () => {
  const newId = Date.now().toString();
  chats.value.unshift({
    id: newId,
    title: `新聊天 ${chats.value.length + 1}`,
    messages: []
  });
  activeChat.value = newId;
  // scrollToBottom();
  showWelcomeScreen.value = false;
};
const handleSelectChat = (chatId) => {
  activeChat.value = chatId;
  showWelcomeScreen.value = false; // 切换到具体聊天时隐藏欢迎页面
  scrollToBottom(); // 滚动到底部
};
//  deleteChat 删除聊天
const deleteChat = (chatId) => {
  const index = chats.value.findIndex((c) => c.id === chatId);
  if (index !== -1) {
    chats.value.splice(index, 1);
    if (activeChat.value === chatId && chats.value.length > 0) {
      activeChat.value = chats.value[0].id;
    } else if (chats.value.length === 0) {
      handleNewChat();
    }
  }
};


const setTitleInputRef = (chatId, el) => {
  if (el) {
    titleInputRefs.value[chatId] = el;
  }
};

// handleEditTitle 编辑聊天标题
const handleEditTitle = (chatId) => {
  const chat = chats.value.find((c) => c.id === chatId);
  if (chat) {
    editingTitle.value = chat.title;
    editingChatId.value = chatId;
    titlePopoverVisible.value[chatId] = true;

    nextTick(() => {
      if (titleInputRefs.value[chatId]) {
        titleInputRefs.value[chatId].focus();
      }
    });
  }
};

// 保存编辑的标题
const confirmEditTitle = () => {
  if (editingChatId.value) {
    const chat = chats.value.find((c) => c.id === editingChatId.value);
    if (chat && editingTitle.value.trim()) {
      chat.title = editingTitle.value.trim();
    }
    titlePopoverVisible.value[editingChatId.value] = false;
    editingChatId.value = null;
  }
};
// 取消编辑
const cancelEditTitle = (chatId) => {
  titlePopoverVisible.value[chatId] = false;
};
// 编辑大标题
const startEditingMainTitle = () => {
  isEditingMainTitle.value = true;
  currentChatTitleEdit.value = currentChatTitle.value;
  nextTick(() => {
    if (mainTitleInput.value) {
      mainTitleInput.value.focus();
    }
  });
};
//  saveMainTitle 保存大标题
const saveMainTitle = () => {
  const chat = chats.value.find((c) => c.id === activeChat.value);
  if (chat && currentChatTitleEdit.value.trim()) {
    chat.title = currentChatTitleEdit.value.trim();
  }
  isEditingMainTitle.value = false;
};
// handleSendMessage 发送消息
const handleSendMessage = () => {
  if (!newMessage.value.trim()) return;

   // 如果是第一次发送消息
   if (showWelcomeScreen.value) {
    showWelcomeScreen.value = false;
    if (chats.value.length === 0) {
      handleNewChat();
    }
  }

  const userMessage = {
    id: Date.now(),
    sender: "user",
    text: newMessage.value,
    time: new Date(),
  };

  const chat = chats.value.find((c) => c.id === activeChat.value);
  if (chat) {
    chat.messages.push(userMessage);
  }

  newMessage.value = "";
  scrollToBottom();

  // AI自动回复
  setTimeout(() => {
    const aiResponses = [
      "系统繁忙，请稍后重试...",
      "很抱歉，我无法回答这个问题。",
      "你真棒！！！"
    ];

    const randomResponse =
      aiResponses[Math.floor(Math.random() * aiResponses.length)];

    const aiMessage = {
      id: Date.now() + 1,
      sender: "ai",
      text: randomResponse,
      time: new Date(),
    };

    if (chat) {
      chat.messages.push(aiMessage);
    }

    scrollToBottom();
  }, 1000);
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesScrollbar.value) {
      messagesScrollbar.value.setScrollTop(99999);
    }
  });
};

const formatTime = (date) => {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

// 侧边栏状态
// const isSidebarCollapsed = ref(false);
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

// 初始化
onMounted(() => {
  showWelcomeScreen.value = true;
  isSidebarCollapsed.value = true;
  chats.value = [];
});

</script>

<style scoped lang="scss">
.chat-page {
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #fff;
  overflow: hidden;
}

.sidebar {
  width: 260px;
  background-color: #fff;
  color: #333;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #ccc;
  z-index: 10;

  &.collapsed {
    width: 70px;

    .sidebar-header h2,
    .chat-history {
      display: none;
    }
  }
}

.sidebar-header {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #eee;

  h2 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }
}

.collapse-btn {
  border: none;
  background: transparent;
  font-size: 18px;
  cursor: pointer;
  color: #666;
  transition: all 0.3s;

  &:hover {
    color: #409eff;
  }
}

.sidebar-content {
  flex: 1;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.new-chat-btn {
  margin-bottom: 16px;

  .el-button {
    width: 100%;
    background-color: #fff;
    border-color: #eee;
    color: #333;

    &:hover {
      background-color: #f5f5f5;
    }
  }
}

.chat-history {
  flex: 1;
  display: flex;
  flex-direction: column;

  .el-menu {
    border-right: none;
    background-color: transparent;
  }

  .el-menu-item {
    height: 44px;
    line-height: 44px;
    margin-bottom: 4px;
    border-radius: 6px;
    display: flex;
    justify-content: space-between;
    background-color: #fff;

    &:hover {
      background-color: #f5f5f5;
    }

    &.is-active {
      background-color: #e6f7ff;
      color: #409eff;
    }

    .chat-actions {
      display: flex;
      margin-left: auto;

      .edit-btn,
      .delete-btn {
        padding: 0;
        color: #999;
        opacity: 0;
        transition: opacity 0.3s;
      }

      .delete-btn:hover {
        color: #f56c6c;
      }
    }

    &:hover .edit-btn,
    &:hover .delete-btn {
      opacity: 1;
    }
  }
}

.sidebar-footer {
  padding: 0 10px;

  .el-button {
    width: 100%;
    background-color: #fff;
    border-color: #eee;
    color: #333;

    &:hover {
      background-color: #f5f5f5;
    }
  }
}

.main-content {
  flex: 1;
  transition: margin-left 0.3s;
  background-color: #fff;
  overflow: hidden;
  position: relative;
  
  &.collapsed {
    margin-left: 70px;
  }
  
  .chat-container {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}

.chat-header {
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fff;

  .chat-title {
    margin: 0;
    font-size: 18px;
    font-weight: 500;
    cursor: pointer;
    text-align: center;
    padding: 0 20px;

    &:hover {
      color: #409eff;
    }
  }

  .title-input {
    width: 300px;

    :deep(.el-input__wrapper) {
      box-shadow: none;
      border-bottom: 1px solid #409eff;
      border-radius: 0;
    }
  }
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow: hidden;
  background-color: #fff;

  .el-scrollbar {
    height: 100%;
  }

  .el-scrollbar__view {
    padding-bottom: 20px;
    max-width: 900px;
    margin: 0 auto;
  }
}

.message {
  display: flex;
  margin-bottom: 20px;

  &.user {
    flex-direction: row-reverse;

    .message-content {
      align-items: flex-end;
    }

    .text {
      background-color: #409eff;
      color: white;
      border-radius: 18px 18px 0 18px;
    }
  }

  &.ai {
    .text {
      background-color: #f5f5f5;
      color: #333;
      border-radius: 18px 18px 18px 0;
    }
  }
}

.avatar {
  margin: 0 12px;

  .el-avatar {
    background-color: #f5f5f5;
    color: #666;
  }
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
}

.text {
  padding: 12px 16px;
  word-break: break-word;
  line-height: 1.5;
  font-size: 15px;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.chat-input {
  padding: 16px 24px;
  background-color: #fff;

  .input-container {
    max-width: 900px;
    margin: 0 auto;
    background-color: #fff;
    
    &.middle {
      width: 700px;
      margin: 0 auto;
    }
  }

  .message-input {
    :deep(.el-textarea__inner) {
      border-radius: 15px;
      padding: 12px 16px;
      box-shadow: none;
      border-color: #eee;
      background-color: #f0f0f0;

      &:focus {
        border-color: #409eff;
        background-color: #ededed;
      }
    }
  }

  .input-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;

    .input-actions-left {
      display: flex;
      gap: 8px;

      .action-btn {
        padding: 0;
        color: #666;

        &:hover {
          color: #409eff;
        }
        
        &.round {
          border-radius: 20px;
        }
      }
    }

    .input-actions-right {
      display: flex;
      align-items: center;
      gap: 8px;

      .action-btn {
        padding: 0;
        color: #666;

        &:hover {
          color: #409eff;
        }
      }

      .send-btn {
        width: 40px;
        height: 40px;
      }
    }
  }

  .ai-tip {
    color: #999;
    font-size: 12px;
    text-align: center;
    margin-top: 8px;
  }
}

.welcome-screen {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px;
  background-color: #fff;
}

.welcome-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.welcome-header {
  margin-bottom: 40px;
  
  h3 {
    font-size: 24px;
    margin-bottom: 16px;
    color: #333;
  }
  
  p {
    font-size: 16px;
    color: #666;
    line-height: 1.6;
  }
}
</style>