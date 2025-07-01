<template>
  <div class="crud-container">
    <!-- 搜索区域 -->
    <el-card shadow="never" class="search-box">
      <el-form :inline="true" :style='{display: "flex", "justify-content": "space-between"}' :model="searchForm" >
        <!-- 搜索表单 -->
        <div class="form-items">
          <el-form-item label="模型名称">
            <el-input 
              v-model="searchForm.modalName" 
              placeholder="请输入关键词" 
              clearable
              @keyup.enter="handleSearch"
              style="width: 200px"
            />
          </el-form-item>

          <el-form-item label="模型状态">
            <el-select 
              :style="{width: '100%'}"
              v-model="searchForm.modalStatus" 
              placeholder="请输入关键词" 
              clearable
              @keyup.enter="handleSearch"
              style="width: 200px"
            >
              <el-option
                v-for="item in modalStatusOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
        </div>

        <el-form-item>
          <el-button type="primary" :icon="Search">搜索</el-button>
          <el-button :icon="Refresh">重置</el-button>
        </el-form-item>

      </el-form>
    </el-card>

    <!-- 表格区域 -->
    <el-card shadow="never" class="table-box">
      <div class="table-header">
        <el-button type="primary" :icon="Plus" @click="handleAdd">新增</el-button>
      </div>
      
      <el-table 
        :data="tableData" 
        v-loading="loading"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="age" label="年龄" width="100" align="center" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="status" label="状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status ? 'success' : 'danger'">
              {{ row.status ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button :style="{padding: 'unset'}" type="primary" text @click="handleEdit(row)">
              配置
            </el-button>
            <el-button :style="{padding: 'unset'}" type="danger" text @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 分页区域 -->
    <!-- <div class="pagination-box">
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[5, 10, 20, 50]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div> -->

    <!-- 新增/编辑弹窗 -->
    <FormDialog 
      v-model="dialogVisible"
      :form-data="currentRow"
      :is-edit="isEditMode"
      @submit="handleSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { model_list } from "@/api/model"
import type { Pagination } from "@/global"
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Search, Refresh, Plus, Delete, Edit } from '@element-plus/icons-vue'
import FormDialog from './FormDialog' 


//
interface TableItem {
  id: string
  modal_name: string
  platform: string
  status: string
  gmt_created: string
}

interface SearchForm {
  modalName: string
  modalStatus:string
}

// 搜索表单-options
const modalStatusOptions: Array<{ label: string, value: string }> = [
  {
    label: "未配置",
    value: "Unconfigured"
  },
  {
    label: "已配置",
    value: "Configured"
  }
]

// 搜索表单数据
const searchForm = reactive<SearchForm>({
  modalName: '',
  modalStatus: ''
})

// 表格数据
const tableData = ref<TableItem[]>([])
const loading = ref(false)

// 分页数据
const pagination = reactive<Pagination>({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

// 对话框控制
const dialogVisible = ref(false)
const currentRow = ref<Partial<TableItem> | null>(null)
const isEditMode = ref(false)

// 模拟数据
const generateMockData = (): TableItem[] => {
  const data: TableItem[] = []
  for (let i = 1; i <= 100; i++) {
    data.push({
      id: i,
      name: `用户${i}`,
      age: Math.floor(Math.random() * 50) + 18,
      address: `地址 ${i} 号`,
      status: Math.random() > 0.5,
      createTime: new Date().toLocaleString()
    })
  }
  return data
}

const mockData = generateMockData()

// 获取表格数据
const fetchData = () => {
  loading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    const { keyword } = searchForm
    const { currentPage, pageSize } = pagination
    
    // 过滤数据
    let filteredData = mockData
    if (keyword) {
      filteredData = mockData.filter(item => item.name.includes(keyword) || item.address.includes(keyword))
    }
    
    // 分页处理
    const start = (currentPage - 1) * pageSize
    const end = start + pageSize
    tableData.value = filteredData.slice(start, end)
    
    // 更新分页总数
    pagination.total = filteredData.length
    loading.value = false
  }, 500)
}

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  fetchData()
}

// 重置
const handleReset = () => {
  searchForm.keyword = ''
  pagination.currentPage = 1
  fetchData()
}

// 新增
const handleAdd = () => {
  currentRow.value = {
    name: '',
    age: null,
    address: '',
    status: true
  }
  isEditMode.value = false
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: TableItem) => {
  currentRow.value = { ...row }
  isEditMode.value = true
  dialogVisible.value = true
}

// 删除
const handleDelete = (row: TableItem) => {
  ElMessageBox.confirm(`确定删除用户 "${row.name}" 吗?`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 实际项目中这里调用API
    ElMessage.success('删除成功')
    fetchData()
  }).catch(() => {})
}

// 分页大小改变
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  fetchData()
}

// 页码改变
const handleCurrentChange = (page: number) => {
  pagination.currentPage = page
  fetchData()
}

// 表单提交
const handleSubmit = (formData: Partial<TableItem>) => {
  if (isEditMode.value) {
    // 更新逻辑
    ElMessage.success('更新成功')
  } else {
    // 新增逻辑
    ElMessage.success('添加成功')
  }
  dialogVisible.value = false
  fetchData()
}

// 初始化加载数据
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.el-form-item {
  margin-bottom: unset !important;
}

.search-box {
  margin-bottom: 10px;
  justify-content: space-between;
}

.table-box {
  margin-bottom: 20px;
}

.table-header {
  margin-bottom: 15px;
}

.pagination-box {
  display: flex;
  justify-content: flex-end;
}
</style>