<template>
  <div class="meeting-detail" v-if="meeting">
    <div class="detail-header">
      <el-button text @click="$router.push('/meetings')"><el-icon><ArrowLeft /></el-icon> 返回列表</el-button>
      <h2>📅 {{ meeting.meeting_time?.split(' ')[0] }} · {{ meeting.title }}</h2>
    </div>

    <el-row :gutter="16">
      <el-col :span="16">
        <el-card shadow="never" class="mb-4">
          <template #header><span class="card-title">基本信息</span></template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="会议类型">{{ meetingTypeLabel(meeting.meeting_type) }}</el-descriptions-item>
            <el-descriptions-item label="主持人">{{ getNickname(meeting.host_id) }}</el-descriptions-item>
            <el-descriptions-item label="日期时间">{{ meeting.meeting_time }}</el-descriptions-item>
            <el-descriptions-item label="时长">{{ meeting.duration_minutes }} 分钟</el-descriptions-item>
            <el-descriptions-item label="参与人" :span="2">{{ meeting.participants.map((p: string) => getNickname(p)).join('、') }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <el-card shadow="never" class="mb-4">
          <template #header><span class="card-title">📋 会议纪要</span></template>
          <div class="markdown-content" v-html="renderMarkdown(meeting.content)"></div>
        </el-card>

        <el-card shadow="never">
          <template #header><span class="card-title">🔗 关联任务</span></template>
          <div v-if="meeting.related_tasks?.length" class="related-tasks">
            <el-tag v-for="t in meeting.related_tasks" :key="t" size="large" class="task-tag" effect="dark">{{ t }}</el-tag>
          </div>
          <el-empty v-else description="暂无关联任务" :image-size="60" />
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never" class="mb-4">
          <template #header><span class="card-title">✅ 决议事项</span></template>
          <div class="decision-list">
            <div v-for="d in meeting.decisions" :key="d.id" class="decision-item">
              <el-checkbox v-model="d.is_resolved" @change="toggleDecision(d)" />
              <span :class="{ resolved: d.is_resolved }">{{ d.content }}</span>
            </div>
            <el-empty v-if="!meeting.decisions?.length" description="暂无决议" :image-size="60" />
          </div>
        </el-card>

        <el-card shadow="never">
          <template #header><span class="card-title">💬 参会人备注</span></template>
          <div class="notes-list">
            <div v-for="(n, i) in meeting.notes" :key="i" class="note-item">{{ n }}</div>
            <el-empty v-if="!meeting.notes?.length" description="暂无备注" :image-size="60" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getMeetingApi, toggleDecisionApi } from '@/api/meeting'
import { mockUsers } from '@/mock/data'

const route = useRoute()
const meeting = ref<any>(null)
const getNickname = (id: string) => mockUsers.find((u) => u.id === id)?.nickname || '未知'
const meetingTypeLabel = (t: string) => ({ daily: '每日站会', weekly: '周会', review: '需求评审', other: '其他' }[t] || t)

const renderMarkdown = (md: string) => {
  if (!md) return ''
  return md
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/\n/g, '<br>')
}

const toggleDecision = async (d: any) => {
  await toggleDecisionApi(meeting.value.id, d.id, d.is_resolved)
}

onMounted(async () => {
  meeting.value = await getMeetingApi(route.params.id as string)
})
</script>

<style scoped>
.detail-header { margin-bottom: 20px; }
.detail-header h2 { margin: 8px 0; color: #e2e8f0; }
.card-title { font-weight: 600; color: #e2e8f0; }
.mb-4 { margin-bottom: 16px; }
.markdown-content { line-height: 1.8; color: #94a3b8; }
.markdown-content :deep(h3) { font-size: 16px; font-weight: 600; margin: 16px 0 8px; color: #e2e8f0; }
.markdown-content :deep(h4) { font-size: 15px; font-weight: 600; margin: 12px 0 6px; color: #e2e8f0; }
.markdown-content :deep(li) { margin-left: 20px; color: #94a3b8; }
.decision-list { display: flex; flex-direction: column; gap: 8px; }
.decision-item { display: flex; align-items: flex-start; gap: 8px; padding: 8px 12px; background: rgba(15, 23, 42, 0.5); border-radius: 8px; border: 1px solid rgba(0, 240, 255, 0.06); color: #e2e8f0; }
.decision-item.resolved { text-decoration: line-through; color: #475569; }
.related-tasks { display: flex; gap: 8px; flex-wrap: wrap; }
.task-tag { cursor: pointer; }
.notes-list { display: flex; flex-direction: column; gap: 8px; }
.note-item { padding: 8px 12px; background: rgba(15, 23, 42, 0.5); border-radius: 8px; border: 1px solid rgba(0, 240, 255, 0.06); font-size: 13px; color: #94a3b8; }
</style>
