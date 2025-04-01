<template>
  <el-form :model="form" @submit.prevent="handleSubmit">
    <el-form-item label="论文来源 URL">
      <el-input v-model="form.url" placeholder="输入要爬取的网页URL"></el-input>
    </el-form-item>
    
    <el-form-item label="筛选标准">
      <el-input
        v-model="form.criteria"
        type="textarea"
        placeholder="输入筛选标准（可选）"
      ></el-input>
    </el-form-item>
    
    <el-form-item label="最大论文数量">
      <el-input-number
        v-model="form.max_papers"
        :min="1"
        :max="50"
      ></el-input-number>
    </el-form-item>
    
    <el-form-item>
      <el-button type="primary" @click="handleSubmit" :loading="loading">
        开始搜索
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  url: '',
  criteria: '',
  max_papers: 20
})

const loading = ref(false)
const emit = defineEmits(['search'])

const handleSubmit = async () => {
  loading.value = true
  emit('search', form.value)
  loading.value = false
}
</script> 