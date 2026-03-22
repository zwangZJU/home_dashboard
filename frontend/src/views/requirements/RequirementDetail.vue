<template>
  <div class="requirement-detail" v-if="req">
    <div class="detail-header">
      <el-button text @click="$router.push('/requirements')"><el-icon><ArrowLeft /></el-icon> 返回列表</el-button>
      <h2>{{ req.req_no }} · {{ req.title }}</h2>
      <div class="header-tags">
        <PriorityTag :priority="req.priority" />
        <StatusBadge :status="req.status" type="requirement" />
      </div>
    </div>

    <el-row :gutter="16">
      <el-col :span="16">
        <el-card shadow="never" class="mb-4">
          <template #header><span class="card-title">基本信息</span></template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="标题">{{ req.title }}</el-descriptions-item>
            <el-descriptions-item label="优先级"><PriorityTag :priority="req.priority" /></el-descriptions-item>
            <el-descriptions-item label="状态"><StatusBadge :status="req.status" type="requirement" /></el-descriptions-item>
            <el-descriptions-item label="提出人">{{ getNickname(req.proposer_id) }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ req.created_at?.split(' ')[0] }}</el-descriptions-item>
            <el-descriptions-item label="预计上线">{{ req.expected_date || '未设置' }}</el-descriptions-item>
          </el-descriptions>
          <div class="mt-4">
            <h4>需求描述</h4>
            <p class="description-text">{{ req.description }}</p>
          </div>
        </el-card>

        <el-card shadow="never">
          <template #header><span class="card-title">需求拆解（子需求）</span></template>
          <div class="sub-req-list">
            <div v-for="child in req.children" :key="child.id" class="sub-req-item">
              <el-checkbox :model-value="child.status === 'done'" disabled />
              <span class="sub-req-title">{{ child.title }}</span>
              <el-tag size="small" :type="child.status === 'done' ? 'success' : 'info'" effect="dark">{{ child.assignee }}</el-tag>
              <StatusBadge :status="child.status" type="requirement" />
            </div>
            <el-empty v-if="!req.children?.length" description="暂无子需求" :image-size="60" />
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never">
          <template #header><span class="card-title">操作历史</span></template>
          <el-timeline>
            <el-timeline-item v-for="(h, i) in req.history" :key="i" :timestamp="h.time" placement="top">
              <div class="history-item">
                <strong>{{ h.operator }}</strong>
                <p>{{ h.action }}</p>
              </div>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getRequirementApi } from '@/api/requirement'
import { mockUsers } from '@/mock/data'
import PriorityTag from '@/components/PriorityTag.vue'
import StatusBadge from '@/components/StatusBadge.vue'

const route = useRoute()
const req = ref<any>(null)
const getNickname = (id: string) => mockUsers.find((u) => u.id === id)?.nickname || '未知'

onMounted(async () => {
  req.value = await getRequirementApi(route.params.id as string)
})
</script>

<style scoped>
.detail-header { margin-bottom: 20px; }
.detail-header h2 { margin: 8px 0; color: #e2e8f0; }
.header-tags { display: flex; gap: 8px; margin-top: 4px; }
.card-title { font-weight: 600; color: #e2e8f0; }
.mb-4 { margin-bottom: 16px; }
.mt-4 { margin-top: 16px; }
.description-text { color: #94a3b8; line-height: 1.8; }
.sub-req-list { display: flex; flex-direction: column; gap: 8px; }
.sub-req-item { display: flex; align-items: center; gap: 12px; padding: 8px 12px; background: rgba(15, 23, 42, 0.5); border-radius: 8px; border: 1px solid rgba(0, 240, 255, 0.06); }
.sub-req-title { flex: 1; color: #e2e8f0; }
.history-item p { color: #64748b; margin: 4px 0 0; }
.history-item strong { color: #e2e8f0; }
</style>
