<template>
  <el-dialog 
    v-model="visible" 
    :title="isEdit ? '编辑用户' : '新增用户'"
    width="600px"
  >
    <el-form 
      ref="formRef" 
      :model="formData" 
      label-width="80px"
      :rules="rules"
    >
      <el-form-item label="姓名" prop="name">
        <el-input v-model="formData.name" placeholder="请输入姓名" />
      </el-form-item>
      
      <el-form-item label="年龄" prop="age">
        <el-input-number 
          v-model="formData.age" 
          :min="1" 
          :max="150"
          controls-position="right"
        />
      </el-form-item>
      
      <el-form-item label="地址" prop="address">
        <el-input 
          v-model="formData.address" 
          placeholder="请输入地址" 
          type="textarea"
          :rows="3"
        />
      </el-form-item>
      
      <el-form-item label="状态" prop="status">
        <el-switch v-model="formData.status" />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="submitForm">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch, type PropType,defineProps,defineEmits } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

const props = defineProps({
  modelValue: Boolean,
  formData: {
    type: Object as PropType<Partial<any>>,
    required: true
  },
  isEdit: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

const visible = ref(props.modelValue)
const formRef = ref<FormInstance>()

// 表单验证规则
const rules = ref<FormRules>({
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 10, message: '长度在2-10个字符', trigger: 'blur' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入地址', trigger: 'blur' }
  ]
})

// 更新visible状态
watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
  if (!val && formRef.value) {
    formRef.value.resetFields()
  }
})

// 确定提交
const submitForm = () => {
  if (!formRef.value) return
  
  formRef.value.validate(valid => {
    if (valid) {
      emit('submit', props.formData)
    }
  })
}
</script>