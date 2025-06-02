<template>
  <el-container class="main-container">
    <!-- 侧边栏 -->
    <el-aside 
      class="sidebar"
      :style="{width: isCollapsed ? '68px' : '260px'}"
    >

      <!-- 侧边栏第一行 -->
      <div class="sidebar-header">
        <div class="text-wrapper">
          <el-icon v-if="!isCollapsed" color="white"><Sugar /></el-icon>
        
          <h3 v-if="!isCollapsed">
            <span>SmartAgent</span>
          </h3>
        </div>
        
        <ExpandBtn :collapse="isCollapsed" @toggle="isCollapsed = !isCollapsed"/>
      </div>

      <!-- 侧边栏第二行 -->
      <NewChatBtn/>

      <!-- 侧边栏最后一行:  -->
      <el-scrollbar class="history-scroll">
        <div class="history-list">
          <div 
            v-for="item in historyList"
            :key="item.id"
            class="history-item"
            :class="{active: item.id === activeHistory}"
          > 
            <div>{{ item.title }}</div>
            <div><el-icon><MoreFilled /></el-icon></div>
          </div>
        </div>
      </el-scrollbar>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="content-container">
      <div class="chat-container">
        <el-header class="header">
          <el-input class="seessionTitle" v-model="sessionTitle"/>
        </el-header>

        <el-main class="chat-main">
          <div 
            v-for="(message, index) in messages"
            :key="index"
            class="message-wrapper"
            :class="{ 'user-message': message.role === 'user' }"
          >
            <div class="message-bubble">
              <div class="message-content">{{ message.content }}</div>
              <div class="message-time">{{ message.time }}</div>
            </div>
          </div>
        </el-main>

        <el-footer class="input-footer">
          <div class="input-wrapper">
            <el-input
              type="textarea"
              :rows="3"
              placeholder="请输入内容..."
              class="input-box"
              :disabled="true"
              resize="none"
            />
            <el-button
              type="primary"
              class="send-btn"
              :disabled="true"
            >
              发送
            </el-button>
          </div>
        </el-footer>
      </div>
    </el-container>
  </el-container>
</template>


<script setup lang="ts">
import { ref } from 'vue'
import ExpandBtn from "./components/ExpandBtn/index.vue"
import NewChatBtn from "./components/NewChatBtn/index.vue"

interface Message {
  role: 'USER' | 'ASSISTANT'
  content: string
}

interface HistoryItem {
  id: number
  title: string
  time: string
}

// 侧边栏状态
const isCollapsed = ref<boolean>(false)

// 会话标题
const sessionTitle = ref<string>("示例标题")

// 消息数据
const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: '你好！我是ChatGPT，有什么可以帮助你的吗？',
    time: '10:00 AM'
  },
  {
    role: 'user',
    content: '请帮我写一个Vue3的示例代码',
    time: '10:01 AM'
  },
  {
    role: 'assistant',
    content: '好的，您需要什么类型的示例？组件示例还是组合式API示例？',
    time: '10:02 AM'
  }
])

// 历史对话数据
const historyList = ref<HistoryItem[]>([
  { id: 1, title: 'Vue3组件示例讨论', time: '10:00' },
  { id: 2, title: 'TypeScript配置问题', time: '09:30' },
  { id: 3, title: '项目结构咨询', time: '09:00' }
])

const activeHistory = ref(1)

const handleNewChat = () => {
  // 新对话逻辑
}
</script>

<style scoped lang="scss">
.main-container {
  overflow: hidden;
  height: 100vh;
}

.sidebar {
  background: #202123;
  transition: width 0.3s;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  max-height: 80px;
  padding: 12px 10px 24px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  
  h3 {
    color: white;
    margin: 0;
  }
}

.text-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.collapse-btn {
  width: 36px;
  height: 36px;
  background: transparent;
  border-color: #444654;
  color: white;
   &:hover {
    background: #343541;
  }
}


.history-scroll {
  flex: 1;
}

.history-list {
  padding: 0 .5rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 38px;
  padding: 0 10px;
  color: #ececf1;
  border-radius: .375rem;
  cursor: pointer;
  font-size: 14px;
  
  &:hover {
    background: #333333;
  }
  
  &.active {
    background: #494949;
  }
}

.content-container {
  background: #292a2d;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  display: flex;
  align-items: center;
}

.chat-main {
  flex: 1;
  padding: 1.25rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.message-wrapper {
  display: flex;
  max-width: 80%;
  
  &.user-message {
    justify-content: flex-end;
    
    .message-bubble {
      background: #409eff;
      color: white;
      
      .message-time {
        color: #e0e0e0;
      }
    }
  }
}

.message-bubble {
  background: white;
  padding: .75rem 1rem;
  border-radius: .75rem;
  box-shadow: 0 .125rem .25rem rgba(0,0,0,0.1);
  max-width: 100%;
  word-break: break-word;
}

.message-content {
  font-size: .875rem;
  line-height: 1.5;
}

.message-time {
  font-size: .75rem;
  color: #666;
  margin-top: .25rem;
  text-align: right;
}

.input-footer {
  padding: 1rem;
  background: white;
  border-top: .0625rem solid #e4e7ed;
}

.input-wrapper {
  display: flex;
  gap: .75rem;
  max-width: 75rem;
  margin: 0 auto;
}

.input-box {
  flex: 1;
  
  :deep(.el-textarea__inner) {
    border-radius: .5rem;
    padding-right: 3.75rem;
    line-height: 1.5;
  }
}

.send-btn {
  height: 2.25rem;
  align-self: flex-end;
  margin-bottom: .5rem;
}


.seessionTitle {
  width: 335px;
  height: 40px;
  margin: 0 auto;

  :deep(.el-input__inner) {
    font-weight: 700;
    font-size: 20px;
    text-align: center;
  }

  :deep(.el-input__wrapper) {
    --el-input-text-color:white ;
    --el-input-hover-border:#525252;
    --el-input-border-color: transparent;
    background-color: transparent;
    text-align: center;
  
  }
}
</style>

<style>
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

::-webkit-scrollbar {
  width: .375rem;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: .25rem;
}

.el-scrollbar__bar.is-vertical {
  width: .375rem;
}

.el-scrollbar__thumb {
  background-color: rgba(144,147,153,.3);
}
</style>