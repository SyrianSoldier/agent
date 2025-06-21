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

        <!-- 聊天会话列表 -->
        <div class="chat-history" v-show="!isSidebarCollapsed">
          <el-scrollbar height="calc(100vh - 180px)">
            <el-menu :default-active="activeChat" @select="handleSelectChat">
              <el-menu-item
                v-for="(chat, index) in messages"
                :key="chat.id"
                :index="chat.id || index"
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
                  <p>
                    我可以帮你呵护你，这次我、写作者的创意内容，请把你的任务交给同学。
                  </p>
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
                        <el-button
                          type="text"
                          :icon="MagicStick"
                          class="action-btn round"
                        >
                          深度思考 (R1)
                        </el-button>
                        <el-button
                          type="text"
                          :icon="Connection"
                          class="action-btn round"
                        >
                          联网搜索
                        </el-button>
                      </div>
                      <div class="input-actions-right">
                        <el-button
                          type="text"
                          :icon="Upload"
                          class="action-btn"
                        />
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
              v-for="message in messages"
              :key="message.id"
              class="message"
              :class="{
                user: message.role === 'USER',
                ai: message.role === 'ASSISTANT',
              }"
            >
              <div class="avatar">
                <el-avatar
                  :icon="message.role === 'USER' ? User : ChatLineRound"
                />
              </div>
              <div class="message-content">
                <div class="text">{{ message.content }}</div>
                <div class="message-time">{{ message.gmt_modified }}</div>
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
                <el-button
                  type="text"
                  :icon="MagicStick"
                  class="action-btn round"
                >
                  深度思考 (R1)
                </el-button>
                <el-button
                  type="text"
                  :icon="Connection"
                  class="action-btn round"
                >
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

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, onUnmounted,reactive, watch } from "vue";
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
  Message,
} from "@element-plus/icons-vue";
import {  ChatWebSocketBaseURL } from "@/constants"
import { create_chat_session } from "@/api/chatSession"
import { type ChatMessage } from "./type"
import { isArray } from "element-plus/es/utils";

const showWelcomeScreen = ref(true) // 控制欢迎页面显示
const isSidebarCollapsed = ref(true) // 侧边栏默认收起

// websocket相关状态
const messages = ref<ChatMessage[]>([])
const socket = ref<WebSocket | null>(null)
const isConnected = ref(false)
const isPulledHistory = ref(false) 
const chatContainer = ref<HTMLElement | null>(null)
const currentSession = reactive<{uuid?: string}>({})
const currentModelName = ref<string | null> ("qwq-plus-latest") // 先默认用qwq-plus-latest, 后面出个下拉框改
const newMessage = ref("")
const activeChat = ref("1")
const messagesScrollbar = ref(null);
const editingTitle = ref("");
const editingChatId = ref(null);
const titlePopoverVisible = ref({});
const titleInputRefs = ref({});
const isEditingMainTitle = ref(false);
const currentChatTitleEdit = ref("");
const mainTitleInput = ref(null);


// 创建会话
const createSession = async () => { 
  try {
    // TODO. 暂时新session的Title用原文字
    const sessionTitle = newMessage.value.trim() 
    const res = await create_chat_session(sessionTitle)
    currentSession.uuid = res.data.uuid
  } catch (error) {
    console.log(error)
  }
}

// 创建ws连接
const connectChatWebsocket = (sessionUuid: string) => {
  if (isConnected.value) {
    return
  }

  const params = `?session_uuid=${sessionUuid}`
  socket.value = new WebSocket(ChatWebSocketBaseURL + "/api/chat" + params)

  socket.value.onopen = () => {
    isConnected.value = true
    console.log("The websocket has been opened with session:", sessionUuid)
  }

  socket.value.onclose = () => {
    isConnected.value = false
    console.log("The websocket has been closed with session:", sessionUuid)
  }

  socket.value.onerror = (error) => {
    console.error('WebSocket error:', error);
  }

  socket.value.onmessage = (event) => {
    let message: any
    let isHistoryMessage = false

    try {
      // 历史消息是数组
      message = JSON.parse(event.data) 
      if (Array.isArray(message)) { 
        isHistoryMessage = true
      }
    } catch { 
      // ai回复是字符串
      message = event.data
      isHistoryMessage = false
    }

    console.log(message)

    if (isHistoryMessage) {
      // 处理历史消息
      console.log("history message:", message)

      const historyMessages: ChatMessage[] = message
      messages.value = [...historyMessages]

      isPulledHistory.value = true
    } else {
      // 处理普通消息
      const messageChunk: string = message

      // 处理ai分块消息
      if (messageChunk === "[CHUNK START]") {
        messages.value.push({
          role: 'ASSISTANT',
          content: message.content,
          gmt_modified: new Date().toISOString()
        })
      } else {
        const lastMessage = messages.value.at(-1)
        lastMessage && (lastMessage.content += messageChunk)
      }
    }

  }
}

// 断开ws连接
const disconnectChatWebsocket = () => {
  if (socket.value && isConnected.value) {
    socket.value.close()
  }
}

// 发送信息给ai
const chatWithAi = () => {
  const params = {
    model_name: currentModelName.value,
    request_params: {
      api_key: localStorage.getItem("api_key")
    },
    messages: newMessage.value.trim()
  }

  socket.value?.send(JSON.stringify(params))
}

// 等待ws连接
const waitForWebSocketConnection = () => {
  return new Promise<void>((resolve, reject) => {
    const checkConnection = () => {
      // 等待连接和拉取历史消息
      if (isConnected.value && isPulledHistory.value) {
        resolve()
      } else {
        setTimeout(checkConnection, 10)
      }
    }

    setTimeout(() => reject("WebSocket connection timeout"), 5000)
    checkConnection()
  })
}

// 发送信息按钮
const handleSendMessage = async () => {
  if (!newMessage.value.trim()) return
  
  // 隐藏聊天页面
  showWelcomeScreen.value = false

  // 如果当前会话不存在,创建新会话
  if (!currentSession.uuid) {
    await createSession()
  }
  
  await waitForWebSocketConnection() // Fix: 直接chatWithAi会出现websocket未连接

  // 视图添加消息
  messages.value.push({
      role: 'USER',
      content: newMessage.value.trim(),
      gmt_modified: new Date().toISOString()
  })
  
  chatWithAi()
}

//  handleNewChat 创建新聊天
const handleNewChat = () => {
  const newId = Date.now().toString();
  chats.value.unshift({
    id: newId,
    title: `新聊天 ${chats.value.length + 1}`,
    messages: [],
  });
  activeChat.value = newId;
  // scrollToBottom();
  showWelcomeScreen.value = false;
}
const handleSelectChat = (chatId) => {
  activeChat.value = chatId;
  showWelcomeScreen.value = false;
  scrollToBottom();
}

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
}

// 取消编辑
const cancelEditTitle = (chatId) => {
  titlePopoverVisible.value[chatId] = false;
}

// 编辑大标题
const startEditingMainTitle = () => {
  isEditingMainTitle.value = true;
  currentChatTitleEdit.value = currentChatTitle.value;
  nextTick(() => {
    if (mainTitleInput.value) {
      mainTitleInput.value.focus();
    }
  });
}

//  saveMainTitle 保存大标题
const saveMainTitle = () => {
  const chat = chats.value.find((c) => c.id === activeChat.value);
  if (chat && currentChatTitleEdit.value.trim()) {
    chat.title = currentChatTitleEdit.value.trim();
  }
  isEditingMainTitle.value = false;
}


const scrollToBottom = () => {
  nextTick(() => {
    if (messagesScrollbar.value) {
      messagesScrollbar.value.setScrollTop(99999);
    }
  });
}


// 侧边栏状态
// const isSidebarCollapsed = ref(false);
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
}

// 监听当前会话, 如果更换会话, 断开老连接,
watch(() => currentSession.uuid, (newVal, oldVal) => {
  if (newVal && newVal !== oldVal) {
    if (socket.value && isConnected.value) {
      disconnectChatWebsocket()
    }
    connectChatWebsocket(newVal)
  }
})

onMounted(() => {
  console.log("mounted")
})

onUnmounted(() => { 
  disconnectChatWebsocket()
})
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
