<template>
  <div class="container">
    <!-- 左侧菜单栏 -->
    <div class="sidebar">
      <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-menu-item 
          v-for="item in menuItem" 
            :key="item.key" 
            :index="item.key"
            :disabled="!!item.disabled" 
            @click="item.onClick"
          >
          {{ item.title }}
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 右侧内容区 -->
    <div class="main-content">
      <router-view/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

interface MenuItem {
  key: string
  title: string               // 标题文本
  disabled?: boolean          // 是否禁用该标题
  onClick?: () => void        // 点击事件
}

const router = useRouter()

const menuItem = ref<MenuItem[]>([
  {
    key: 'model_config',
    title: '模型配置',
    onClick: () => {
      router.push({"path": "/workspace/modelConfig"})
    }
  }
])


const handleOpen = (key: string, keyPath: string[]) => {
  console.log('菜单展开:', key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log('菜单收起:', key, keyPath)
}

</script>

<style scoped lang="scss">
.container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 240px;
  height: 100%;
  background-color: #fff;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
  
  .el-menu {
    height: 100%;
    border-right: none;
  }
}

.main-content {
  flex: 1;
  padding: 10px;
  background-color: #f5f7fa;
  overflow-y: auto;
}
</style>