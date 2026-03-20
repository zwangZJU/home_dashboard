<template>
  <div class="progress-page">
    <div class="page-header">
      <h2>📊 进度展示</h2>
      <el-radio-group v-model="activeView" class="view-toggle">
        <el-radio-button value="timeline">时间线</el-radio-button>
        <el-radio-button value="burndown">燃尽图</el-radio-button>
        <el-radio-button value="members">成员工作量</el-radio-button>
      </el-radio-group>
    </div>

    <!-- Overview -->
    <el-card shadow="hover" class="mb-4">
      <template #header><span class="card-title">📈 项目进度概览</span></template>
      <div class="overview">
        <div class="overview-main">
          <span class="overview-label">总体完成率</span>
          <el-progress :percentage="completionRate" :stroke-width="20" :text-inside="true" style="max-width: 400px" />
        </div>
        <div class="overview-stats">
          <div class="stat">需求完成: <strong>{{ completedReqs }}/{{ totalReqs }}</strong></div>
          <div class="stat">任务完成: <strong>{{ completedTasks }}/{{ totalTasks }}</strong></div>
        </div>
      </div>
    </el-card>

    <!-- Timeline / Gantt -->
    <el-card v-show="activeView === 'timeline'" shadow="hover" class="mb-4">
      <template #header><span class="card-title">📅 甘特图 / 时间线</span></template>
      <div ref="ganttRef" style="height: 300px"></div>
    </el-card>

    <!-- Burndown -->
    <el-card v-show="activeView === 'burndown'" shadow="hover" class="mb-4">
      <template #header><span class="card-title">📉 燃尽图（Sprint 视角）</span></template>
      <div ref="burndownRef" style="height: 300px"></div>
    </el-card>

    <!-- Member Workload -->
    <el-card v-show="activeView === 'members'" shadow="hover">
      <template #header><span class="card-title">👥 成员工作量</span></template>
      <el-row :gutter="16">
        <el-col :span="12">
          <div ref="memberChartRef" style="height: 280px"></div>
        </el-col>
        <el-col :span="12">
          <div class="member-list">
            <div v-for="m in memberWorkload" :key="m.user.id" class="member-item">
              <el-avatar :size="36">{{ m.user.nickname[0] }}</el-avatar>
              <div class="member-info">
                <div class="member-name">{{ m.user.nickname }}</div>
                <div class="member-detail">{{ m.total }} 任务 ({{ m.done }}完成, {{ m.inProgress }}进行中)</div>
              </div>
              <el-progress :percentage="m.total ? Math.round(m.done / m.total * 100) : 0" :stroke-width="8" style="width: 100px" />
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getTimelineDataApi, getBurndownDataApi, getMemberWorkloadApi } from '@/api/progress'
import { getTasksApi } from '@/api/task'
import { getRequirementsApi } from '@/api/requirement'

const activeView = ref('timeline')
const ganttRef = ref<HTMLElement>()
const burndownRef = ref<HTMLElement>()
const memberChartRef = ref<HTMLElement>()

const completionRate = ref(0)
const completedReqs = ref(0)
const totalReqs = ref(0)
const completedTasks = ref(0)
const totalTasks = ref(0)
const memberWorkload = ref<any[]>([])

let ganttChart: any, burndownChart: any, memberChart: any

const initCharts = async () => {
  // Overview
  const allTasks = await getTasksApi() as any[]
  const allReqs = await getRequirementsApi() as any[]
  totalTasks.value = allTasks.length
  completedTasks.value = allTasks.filter((t) => t.status === 'done').length
  totalReqs.value = allReqs.length
  completedReqs.value = allReqs.filter((r) => r.status === 'done').length
  completionRate.value = totalTasks.value ? Math.round(completedTasks.value / totalTasks.value * 100) : 0

  // Timeline / Gantt
  const timelineData = await getTimelineDataApi() as any[]
  if (ganttRef.value) {
    ganttChart = echarts.init(ganttRef.value)
    ganttChart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      xAxis: { type: 'value' },
      yAxis: { type: 'category', data: timelineData.map((d) => d.name) },
      series: [
        {
          type: 'custom', name: '实际进度',
          renderItem: (_params: any, api: any) => {
            const categoryIndex = api.value(0)
            const start = api.coord([api.value(1), categoryIndex])
            const end = api.coord([api.value(2), categoryIndex])
            const height = api.size([0, 1])[1] * 0.4
            return {
              type: 'rect', shape: { x: start[0], y: start[1] - height / 2, width: end[0] - start[0], height },
              style: { fill: api.value(4) === 'done' ? '#67C23A' : '#409EFF' },
            }
          },
          encode: { x: [1, 2], y: 0 },
          data: timelineData.map((d) => [d.name, d.start, d.end, d.progress, d.status]),
        },
      ],
      grid: { left: 160, right: 40, bottom: 40, top: 20 },
    })
  }

  // Burndown
  const burnData = await getBurndownDataApi() as any
  if (burndownRef.value) {
    burndownChart = echarts.init(burndownRef.value)
    burndownChart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: ['理想线', '实际线'] },
      xAxis: { type: 'category', data: burnData.days },
      yAxis: { type: 'value', minInterval: 1 },
      series: [
        { name: '理想线', type: 'line', data: burnData.ideal, smooth: true, lineStyle: { type: 'dashed', color: '#909399' } },
        { name: '实际线', type: 'line', data: burnData.actual, smooth: true, areaStyle: { opacity: 0.15 }, itemStyle: { color: '#409EFF' } },
      ],
      grid: { left: 40, right: 20, bottom: 30, top: 40 },
    })
  }

  // Members
  memberWorkload.value = await getMemberWorkloadApi() as any[]
  if (memberChartRef.value) {
    memberChart = echarts.init(memberChartRef.value)
    memberChart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: memberWorkload.value.map((m) => m.user.nickname) },
      yAxis: { type: 'value', minInterval: 1 },
      series: [
        { name: '已完成', type: 'bar', stack: 'total', data: memberWorkload.value.map((m) => m.done), itemStyle: { color: '#67C23A' } },
        { name: '进行中', type: 'bar', stack: 'total', data: memberWorkload.value.map((m) => m.inProgress), itemStyle: { color: '#409EFF' } },
        { name: '待开始', type: 'bar', stack: 'total', data: memberWorkload.value.map((m) => m.total - m.done - m.inProgress), itemStyle: { color: '#E6A23C' } },
      ],
      legend: { data: ['已完成', '进行中', '待开始'] },
      grid: { left: 40, right: 20, bottom: 30, top: 40 },
    })
  }
}

onMounted(() => nextTick(initCharts))
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { margin: 0; }
.mb-4 { margin-bottom: 16px; }
.card-title { font-weight: 600; }
.overview { display: flex; justify-content: space-between; align-items: center; }
.overview-main { flex: 1; }
.overview-label { font-size: 14px; color: #606266; margin-bottom: 8px; display: block; }
.overview-stats { display: flex; gap: 24px; }
.stat { font-size: 14px; color: #606266; }
.stat strong { color: #303133; }
.member-list { display: flex; flex-direction: column; gap: 16px; padding: 12px 0; }
.member-item { display: flex; align-items: center; gap: 12px; padding: 12px; background: #fafafa; border-radius: 10px; }
.member-name { font-weight: 600; font-size: 14px; }
.member-detail { font-size: 12px; color: #909399; }
.member-info { flex: 1; }
</style>
