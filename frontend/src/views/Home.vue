
<template>
  <div class="home">
    <!-- 添加一个带边框的容器 -->
    <div class="content-container">
      <el-container>
        <el-header>
          <h1>顶会论文搜索与分析</h1>
        </el-header>
        
          <el-main>
          <el-form :model="form" @submit.prevent="handleSubmit">
            <el-form-item label="论文来源 URL">
              <el-input 
                v-model="form.url" 
                placeholder="https://papers.cool/venue/NeurIPS.2024?group=Oral">
              </el-input>
            </el-form-item>
            
            <el-form-item label="筛选标准">
              <el-input
                v-model="form.criteria"
                type="textarea"
                placeholder="关于多模态视觉语言模型的论文">
              </el-input>
            </el-form-item>
            
            <el-form-item label="最大论文数量">
              <el-input-number
                v-model="form.max_papers"
                :min="1"
                :max="1000"
                :step="1">
              </el-input-number>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="handleSubmit" :loading="loading">
                开始搜索
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 显示结果 -->
          <div v-if="papers.length" class="paper-list">
            <el-card v-for="paper in papers" :key="paper.url" class="paper-card">
              <template #header>
                <div class="card-header">
                  <h3>{{ paper.title }}</h3>
                </div>
              </template>
              
              <el-tabs>
                <el-tab-pane label="中文摘要">
                  <p>{{ paper.abstract_zh }}</p>
                </el-tab-pane>
                <el-tab-pane label="英文摘要">
                  <p>{{ paper.abstract_en }}</p>
                </el-tab-pane>
              </el-tabs>

              <div v-if="paper.problems_solved" class="analysis">
                <h4>解决的问题：</h4>
                <ul>
                  <li v-for="(problem, index) in paper.problems_solved" :key="index">
                    {{ problem }}
                  </li>
                </ul>
              </div>

              <div v-if="paper.innovations" class="analysis">
                <h4>创新点：</h4>
                <ul>
                  <li v-for="(innovation, index) in paper.innovations" :key="index">
                    {{ innovation }}
                  </li>
                </ul>
              </div>

              <div class="actions">
                <el-button type="primary" @click="openPaper(paper.url)">
                  查看原文
                </el-button>
              </div>
            </el-card>
          </div>
        </el-main>
      </el-container>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 修改为后端服务地址，如果要使用ngrok，则修改为ngrok的地址
const API_BASE_URL = 'https://575f-2403-d400-1201-ff8-00-7d8.ngrok-free.app'  // 本地开发时使用 8000 端口

const form = ref({
  url: '',
  criteria: '',
  max_papers: 20
})

const papers = ref([])
const loading = ref(false)

// 不映射
// const handleSubmit = async () => {
//   if (!form.value.url) {
//     ElMessage.warning('请输入URL')
//     return
//   }

//   loading.value = true
//   try {
//     const response = await axios.post('http://localhost:8000/api/papers', form.value)
//     papers.value = response.data.papers
//     ElMessage.success(`成功获取 ${papers.value.length} 篇论文`)
//   } catch (error) {
//     ElMessage.error(error.response?.data?.error || '请求失败')
//   } finally {
//     loading.value = false
//   }
// }


const handleSubmit = async () => {
  if (!form.value.url) {
    ElMessage.warning('请输入URL')
    return
  }

  loading.value = true
  try {
    const response = await axios.post(`${API_BASE_URL}/api/papers`, form.value)
    papers.value = response.data.papers
    ElMessage.success(`成功获取 ${papers.value.length} 篇论文`)
  } catch (error) {
    console.error('Error:', error)
    ElMessage.error(error.response?.data?.error || '请求失败')
  } finally {
    loading.value = false
  }
}

const openPaper = (url) => {
  window.open(url, '_blank')
}
</script>

<style scoped>
/* 已有的样式保持不变 */

/* 添加输入框样式 */
:deep(.el-input__wrapper) {
  background-color: #1a1a1a !important;  /* 黑色背景 */
  box-shadow: 0 0 0 1px #ffffff !important;  /* 白色边框 */
}

:deep(.el-input__inner) {
  color: #ffffff !important;  /* 白色文字 */
}

/* 文本域样式 */
:deep(.el-textarea__inner) {
  background-color: #1a1a1a !important;
  color: #ffffff !important;
  border: 1px solid #ffffff !important;
}

/* 数字输入框样式 */
:deep(.el-input-number__decrease),
:deep(.el-input-number__increase) {
  background-color: #1a1a1a !important;
  color: #ffffff !important;
  border-color: #ffffff !important;
}

/* placeholder 文字颜色 */
:deep(.el-input__inner::placeholder),
:deep(.el-textarea__inner::placeholder) {
  color: #909399 !important;
}

/* 添加标题居中样式 */
.el-header {
  text-align: center;  /* 文字居中 */
  padding: 20px 0;     /* 上下添加一些间距 */
}

h1 {
  color: #409EFF;
  margin: 0;          /* 移除默认边距 */
}
</style>