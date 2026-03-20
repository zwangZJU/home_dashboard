<template>
  <div class="dashboard">
    <!-- Stats Cards -->
    <el-row :gutter="16" class="mb-6">
      <el-col :span="6" v-for="card in statCards" :key="card.label">
        <el-card shadow="hover" class="stat-card" @click="$router.push(card.route)">
          <div class="stat-content">
            <div class="stat-icon" :style="{ background: card.bg }">
              <el-icon :size="24" :color="card.color"><component :is="card.icon" /></el-icon>
            </div>
            <div>
              <div class="stat-value">{{ card.value }}</div>
              <div class="stat-label">{{ card.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="mb-6">
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header><span class="card-title">📈 需求完成趋势（近30天）</span></template>
          <div ref="trendChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header><span class="card-title">📅 近期会议</span></template>
          <div class="meeting-list">
            <div v-for="m in meetings.slice(0, 5)" :key="m.id" class="meeting-item" @click="$router.push(`/meetings/${m.id}`)">
              <el-icon class="meeting-icon"><Calendar /></el-icon>
              <div class="meeting-info">
                <div class="meeting-title">{{ m.title }}</div>
                <div class="meeting-meta">{{ m.meeting_time?.split(' ')[0] }} · {{ getNickname(m.host_id) }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16">
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header><span class="card-title">🔥 紧急任务（高优先级）</span></template>
          <el-table :data="urgentTasks" size="small" stripe>
            <el-table-column prop="task_no" label="编号" width="100" />
            <el-table-column prop="title" label="标题" />
            <el-table-column label="优先级" width="80">
              <template #default="{ row }"><PriorityTag :priority="row.priority" /></template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }"><StatusBadge :status="row.status" type="task" /></template>
            </el-table-column>
            <el-table-column label="截止日期" width="120">
              <template #default="{ row }">
                <span :class="{ 'text-danger': isOverdue(row.due_date) }">{{ row.due_date }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header><span class="card-title">⏰ 近期截止任务</span></template>
          <div class="deadline-list">
            <div v-for="t in upcomingTasks" :key="t.id" class="deadline-item">
              <div class="deadline-title">{{ t.title }}</div>
              <el-tag size="small" :type="isOverdue(t.due_date) ? 'danger' : 'info'">
                {{ t.due_date }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStatsApi, getTrendDataApi } from '@/api/progress'
import { getTasksApi } from '@/api/task'
import { getMeetingsApi } from '@/api/meeting'
import { mockUsers } from '@/mock/data'
import PriorityTag from '@/components/PriorityTag.vue'
import StatusBadge from '@/components/StatusBadge.vue'

const stats = ref<any>({})
const trendData = ref<any[]>([])
const tasks = ref<any[]>([])
const meetings = ref<any[]>([])
const trendChartRef = ref<HTMLElement>()

const statCards = computed(() => [
  { label: '总需求', value: stats.value.total_requirements || 0, icon: 'Document', color: '#409EFF', bg: '#ecf5ff', route: '/requirements' },
  { label: '进行中', value: stats.value.active_tasks || 0, icon: 'Loading', color: '#E6A23C', bg: '#fdf6ec', route: '/tasks' },
  { label: '已完成', value: stats.value.completed_tasks || 0, icon: 'CircleCheck', color: '#67C23A', bg: '#f0f9eb', route: '/tasks' },
  { label: '已逾期', value: stats.value.overdue_tasks || 0, icon: 'WarningFilled', color: '#F56C6C', bg: '#fef0f0', route: '/tasks' },
])

const urgentTasks = computed(() => tasks.value.filter((t: any) => t.priority === 'high').slice(0, 10))
const upcomingTasks = computed(() =>
  tasks.value.filter((t: any) => t.status !== 'done' && t.due_date).sort((a: any, b: any) => a.due_date.localeCompare(b.due_date)).slice(0, 8)
)

const getNickname = (id: string) => mockUsers.find((u) => u.id === id)?.nickname || '未知'
const isOverdue = (date: string) => date && date < new Date().toISOString().split('T')[0]

onMounted(async () => {
  stats.value = await getDashboardStatsApi()
  trendData.value = await getTrendDataApi()
  tasks.value = await getTasksApi()
  meetings.value = await getMeetingsApi()

  if (trendChartRef.value) {
    const chart = echarts.init(trendChartRef.value)
    chart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: trendData.value.map((d) => d.date) },
      yAxis: { type: 'value', minInterval: 1 },
      series: [{ name: '完成数', type: 'line', data: trendData.value.map((d) => d.count), smooth: true, areaStyle: { opacity: 0.15 }, itemStyle: { color: '#409EFF' } }],
      grid: { left: 40, right: 20, bottom: 30, top: 20 },
    })
  }
})
</script>

<style scoped>
.stat-card { cursor: pointer; transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-2px); }
.stat-content { display: flex; align-items: center; gap: 16px; }
.stat-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.stat-value { font-size: 28px; font-weight: 700; color: #303133; }
.stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
.card-title { font-size: 15px; font-weight: 600; }
.mb-6 { margin-bottom: 24px; }
.meeting-list { display: flex; flex-direction: column; gap: 12px; }
.meeting-item { display: flex; align-items: center; gap: 12px; padding: 8px; border-radius: 8px; cursor: pointer; transition: background 0.2s; }
.meeting-item:hover { background: #f5f7fa; }
.meeting-icon { color: #409EFF; font-size: 18px; }
.meeting-title { font-weight: 500; color: #303133; }
.meeting-meta { font-size: 12px; color: #909399; margin-top: 2px; }
.deadline-list { display: flex; flex-direction: column; gap: 10px; }
.deadline-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: #fafafa; border-radius: 8px; }
.deadline-title { font-size: 14px; color: #303133; }
.text-danger { color: #F56C6C; font-weight: 600; }
</style>
