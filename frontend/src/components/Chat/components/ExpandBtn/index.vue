<template>
  <el-button
    circle
    class="collapse-btn"
    @click="handleClick"
    :style="{ fontSize: `${fontSize}px` }"
  >
    <el-icon>
      <component :is="props.collapse ? 'Expand' : 'Fold'" />
    </el-icon> 
  </el-button>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'

const props = defineProps({
  collapse: {
    type: Boolean,
    default: false
  },

  fontSize: {
    type: String,
    default: "18"
  }
})
const emit = defineEmits(["toggle"])


const handleClick = () => emit("toggle")

</script>

<style scoped lang="scss">

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
</style>