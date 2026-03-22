<template>
  <div class="meeting-list-page">
    <div class="page-header">
      <h2>📝 会议纪要</h2>
      <el-button type="primary" @click="showCreateDialog = true"><el-icon><Plus /></el-icon> 新建会议</el-button>
    </div>

    <div class="meeting-cards">
      <div v-for="m in meetings" :key="m.id" class="meeting-card" @click="$router.push(`/meetings/${m.id}`)">
        <div class="meeting-card-header">
          <span class="meeting-date">📅 {{ m.meeting_time?.split(' ')[0] }}</span>
          <el-tag size="small" effect="dark">{{ meetingTypeLabel(m.meeting_type) }}</el-tag>
        </div>
        <h3 class="meeting-card-title">{{ m.title }}</h3>
        <div class="meeting-card-meta">
          <span>参会: {{ m.participants.map((p: string) => getNickname(p)).join('、') }}</span>
          <span>待办决策: {{ m.decisions?.filter((d: any) => !d.is_resolved).length || 0 }} 项</span>
          <span>关联任务: {{ m.related_tasks?.length || 0 }} 项</span>
        </div>
        <div class="meeting-card-action">
          <el-button type="primary" text>查看详情 →</el-button>
        </div>
      </div>
    </div>

    <el-empty v-if="meetings.length === 0" description="暂无会议纪要" />

    <!-- Create Dialog -->
    <el-dialog v-model="showCreateDialog" title="新建会议" width="600px">
      <el-form :model="createForm" label-width="100px">
        <el-form-item label="会议标题" required><el-input v-model="createForm.title" /></el-form-item>
        <el-form-item label="会议类型">
          <el-select v-model="createForm.meeting_type" style="width: 100%">
            <el-option label="每日站会" value="daily" /><el-option label="周会" value="weekly" />
            <el-option label="需求评审" value="review" /><el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="会议时间">
          <el-date-picker v-model="createForm.meeting_time" type="datetime" value-format="YYYY-MM-DD HH:mm" style="width: 100%" />
        </el-form-item>
        <el-form-item label="时长（分钟）"><el-input-number v-model="createForm.duration_minutes" :min="15" :step="15" /></el-form-item>
        <el-form-item label="纪要内容"><el-input v-model="createForm.content" type="textarea" :rows="6" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getMeetingsApi, createMeetingApi } from '@/api/meeting'
import { mockUsers } from '@/mock/data'
import { ElMessage } from 'element-plus'

const meetings = ref<any[]>([])
const showCreateDialog = ref(false)
const getNickname = (id: string) => mockUsers.find((u) => u.id === id)?.nickname || '未知'
const meetingTypeLabel = (t: string) => ({ daily: '每日站会', weekly: '周会', review: '需求评审', other: '其他' }[t] || t)

const createForm = reactive({ title: '', meeting_type: 'weekly', meeting_time: '', duration_minutes: 60, content: '' })

const handleCreate = async () => {
  if (!createForm.title) { ElMessage.warning('请填写标题'); return }
  await createMeetingApi({ ...createForm, host_id: '1', participants: ['1', '2', '3'] })
  ElMessage.success('创建成功')
  showCreateDialog.value = false
  meetings.value = await getMeetingsApi() as any[]
}

onMounted(async () => { meetings.value = await getMeetingsApi() as any[] })
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { margin: 0; color: #e2e8f0; }
.meeting-cards { display: flex; flex-direction: column; gap: 12px; }
.meeting-card {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 240, 255, 0.1);
  border-radius: 12px; padding: 20px;
  cursor: pointer; transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.03);
}
.meeting-card:hover {
  transform: translateY(-1px);
  border-color: rgba(0, 240, 255, 0.25);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.08);
}
.meeting-card-header { display: flex; justify-content: space-between; align-items: center; }
.meeting-date { font-size: 14px; color: #00f0ff; font-weight: 600; text-shadow: 0 0 6px rgba(0, 240, 255, 0.3); }
.meeting-card-title { font-size: 16px; font-weight: 600; margin: 8px 0; color: #e2e8f0; }
.meeting-card-meta { display: flex; gap: 20px; font-size: 13px; color: #64748b; }
.meeting-card-action { margin-top: 8px; }
</style>
