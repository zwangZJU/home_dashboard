<template>
  <div class="dashboard">
    <!-- Stats Cards -->
    <el-row :gutter="16" class="mb-6">
      <el-col :span="6" v-for="card in statCards" :key="card.label">
        <div class="stat-card" :class="`stat-card-${card.theme}`" @click="$router.push(card.route)">
          <div class="stat-glow"></div>
          <div class="stat-content">
            <div class="stat-icon" :style="{ background: card.bg, color: card.color }">
              <el-icon :size="24"><component :is="card.icon" /></el-icon>
            </div>
            <div>
              <div class="stat-value">{{ card.value }}</div>
              <div class="stat-label">{{ card.label }}</div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="mb-6">
      <el-col :span="14">
        <el-card shadow="never">
          <template #header><span class="card-title">📈 需求完成趋势（近30天）</span></template>
          <div ref="trendChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="never">
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
        <el-card shadow="never">
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
        <el-card shadow="never">
          <template #header><span class="card-title">⏰ 近期截止任务</span></template>
          <div class="deadline-list">
            <div v-for="t in upcomingTasks" :key="t.id" class="deadline-item">
              <div class="deadline-title">{{ t.title }}</div>
              <el-tag size="small" :type="isOverdue(t.due_date) ? 'danger' : 'info'" effect="dark">
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
  { label: '总需求', value: stats.value.total_requirements || 0, icon: 'Document', color: '#00f0ff', bg: 'rgba(0, 240, 255, 0.1)', theme: 'cyan', route: '/requirements' },
  { label: '进行中', value: stats.value.active_tasks || 0, icon: 'Loading', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)', theme: 'amber', route: '/tasks' },
  { label: '已完成', value: stats.value.completed_tasks || 0, icon: 'CircleCheck', color: '#22c55e', bg: 'rgba(34, 197, 94, 0.1)', theme: 'green', route: '/tasks' },
  { label: '已逾期', value: stats.value.overdue_tasks || 0, icon: 'WarningFilled', color: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)', theme: 'red', route: '/tasks' },
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
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        borderColor: 'rgba(0, 240, 255, 0.2)',
        textStyle: { color: '#e2e8f0' },
      },
      xAxis: {
        type: 'category',
        data: trendData.value.map((d) => d.date),
        axisLine: { lineStyle: { color: 'rgba(0, 240, 255, 0.15)' } },
        axisLabel: { color: '#64748b' },
        splitLine: { show: false },
      },
      yAxis: {
        type: 'value',
        minInterval: 1,
        axisLine: { show: false },
        axisLabel: { color: '#64748b' },
        splitLine: { lineStyle: { color: 'rgba(0, 240, 255, 0.06)' } },
      },
      series: [{
        name: '完成数',
        type: 'line',
        data: trendData.value.map((d) => d.count),
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { color: '#00f0ff', width: 2, shadowColor: 'rgba(0, 240, 255, 0.3)', shadowBlur: 10 },
        itemStyle: { color: '#00f0ff' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(0, 240, 255, 0.25)' },
            { offset: 1, color: 'rgba(0, 240, 255, 0)' },
          ]),
        },
      }],
      grid: { left: 40, right: 20, bottom: 30, top: 20 },
    })
  }
})
</script>

<style scoped>
.mb-6 { margin-bottom: 24px; }
.card-title { font-size: 15px; font-weight: 600; }

/* Stat cards with glow accent */
.stat-card {
  position: relative;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 240, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}
.stat-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  border-radius: 0 2px 2px 0;
}
.stat-card-cyan::before { background: #00f0ff; box-shadow: 0 0 10px rgba(0, 240, 255, 0.5); }
.stat-card-amber::before { background: #f59e0b; box-shadow: 0 0 10px rgba(245, 158, 11, 0.5); }
.stat-card-green::before { background: #22c55e; box-shadow: 0 0 10px rgba(34, 197, 94, 0.5); }
.stat-card-red::before { background: #ef4444; box-shadow: 0 0 10px rgba(239, 68, 68, 0.5); }
.stat-card:hover {
  transform: translateY(-3px);
  border-color: rgba(0, 240, 255, 0.25);
  box-shadow: 0 0 25px rgba(0, 240, 255, 0.08);
}
.stat-content { display: flex; align-items: center; gap: 16px; }
.stat-icon {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
}
.stat-value {
  font-size: 28px; font-weight: 700;
  background: linear-gradient(135deg, #e2e8f0, #94a3b8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-label { font-size: 13px; color: #94a3b8; margin-top: 4px; }

/* Meeting list */
.meeting-list { display: flex; flex-direction: column; gap: 12px; }
.meeting-item {
  display: flex; align-items: center; gap: 12px; padding: 10px 12px;
  border-radius: 10px; cursor: pointer; transition: all 0.3s ease;
  border: 1px solid transparent;
}
.meeting-item:hover {
  background: rgba(0, 240, 255, 0.05);
  border-color: rgba(0, 240, 255, 0.15);
}
.meeting-icon { color: #00f0ff; font-size: 18px; }
.meeting-title { font-weight: 500; color: #e2e8f0; }
.meeting-meta { font-size: 12px; color: #64748b; margin-top: 2px; }

/* Deadline list */
.deadline-list { display: flex; flex-direction: column; gap: 10px; }
.deadline-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 14px; background: rgba(15, 23, 42, 0.5);
  border-radius: 10px; border: 1px solid rgba(0, 240, 255, 0.06);
  transition: all 0.3s ease;
}
.deadline-item:hover {
  border-color: rgba(0, 240, 255, 0.15);
}
.deadline-title { font-size: 14px; color: #e2e8f0; }
.text-danger { color: #ef4444 !important; font-weight: 600; }
</style>
