<template>
  <el-card class="paper-card">
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

    <div class="analysis">
      <h4>解决的问题：</h4>
      <ul>
        <li v-for="(problem, index) in paper.problems_solved" :key="index">
          {{ problem }}
        </li>
      </ul>

      <h4>创新点：</h4>
      <ul>
        <li v-for="(innovation, index) in paper.innovations" :key="index">
          {{ innovation }}
        </li>
      </ul>
    </div>

    <div class="actions">
      <el-button type="primary" @click="openPaper">查看原文</el-button>
    </div>
  </el-card>
</template>

<script setup>
const props = defineProps({
  paper: {
    type: Object,
    required: true
  }
})

const openPaper = () => {
  window.open(props.paper.url, '_blank')
}
</script>

<style scoped>
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
</style> 