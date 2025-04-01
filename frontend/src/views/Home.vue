<template>
  <div class="home">
    <el-container>
      <el-header>
        <h1>论文搜索与分析</h1>
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
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const form = ref({
  url: '',
  criteria: '',
  max_papers: 20
})

const papers = ref([])
const loading = ref(false)

const handleSubmit = async () => {
  if (!form.value.url) {
    ElMessage.warning('请输入URL')
    return
  }

  loading.value = true
  try {
    const response = await axios.post('http://localhost:8000/api/papers', form.value)
    papers.value = response.data.papers
    ElMessage.success(`成功获取 ${papers.value.length} 篇论文`)
  } catch (error) {
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
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.el-header {
  text-align: center;
  padding: 20px;
}

.paper-list {
  margin-top: 20px;
}

.paper-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.analysis {
  margin-top: 20px;
}

.actions {
  margin-top: 20px;
  text-align: right;
}

h1 {
  color: #409EFF;
}
</style>