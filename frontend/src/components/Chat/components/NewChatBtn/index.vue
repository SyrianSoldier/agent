<template>
  <el-button
    type="primary"
    class="new-chat-btn"
    color="#4d6bfe"
    @click="handleClick"
  >
    <el-icon><ChatRound /></el-icon>
    <span>开启新对话</span>
  </el-button>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'

const props = defineProps({
  
})
const emit = defineEmits(["newChat"])


const handleClick = () => emit("newChat")

</script>

<style scoped lang="scss">

.new-chat-btn {
  width: 131px !important;
  height: 44px;
  border-radius: 14px;
  flex-shrink: 0;
  align-items: center;
  width: fit-content;
  margin: 0 2px 0 14px;
  font-size: 16px;
  font-weight: 500;
  line-height: 20px;
  display: flex;
  overflow: hidden;
  margin-bottom: 34px;
}
</style>