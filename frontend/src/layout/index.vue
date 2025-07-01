
<template>
  <div class="container">
    <!-- 顶部导航栏 -->
    <el-menu
      :default-active="activeIndex"
      class="header"
      mode="horizontal"
      @select="handleSelect"
    >
      
      <el-menu-item 
        v-for="item in MenuItems" 
          :key="item.key" 
          :index="item.key"
          :disabled="!!item.disabled" 
          @click="item.onClick"
        >
        {{ item.title }}
      </el-menu-item>
    </el-menu>

    <div class="main">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

interface MenuItem {
  key: string
  title: string               // 标题文本
  disabled?: boolean          // 是否禁用该标题
  onClick?: () => void        // 点击事件
}

const activeIndex = ref('chat')

const MenuItems = ref<MenuItem[]>([
  {
    key: 'chat',
    title: '聊天',
    onClick: () => {
      activeIndex.value = 'chat'
      router.push({path: "/chat"})
    }
  },
  {
    key: 'workspace',
    title: '工作区',
    onClick: () => {
      activeIndex.value = 'workspace'
      router.push({path: "/workspace"})
    }
  }
])

const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

</script>

<style scoped lang="scss">
.container {
  height: 100vh;
  font-family: Arial, sans-serif;
}

.header {
  height: 45px;
}

.main {
  height: calc(100vh - 45px);
  overflow: hidden;
}
</style>