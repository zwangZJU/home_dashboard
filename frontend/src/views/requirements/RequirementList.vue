<template>
  <div class="requirement-list">
    <div class="page-header">
      <h2>📋 需求管理</h2>
      <div class="header-actions">
        <el-input v-model="search" placeholder="搜索需求..." prefix-icon="Search" style="width: 240px" clearable @input="loadRequirements" />
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon> 新建需求
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeFilter" @tab-change="loadRequirements">
      <el-tab-pane label="全部" name="all" />
      <el-tab-pane label="草稿" name="draft" />
      <el-tab-pane label="待评审" name="review" />
      <el-tab-pane label="已通过" name="approved" />
      <el-tab-pane label="开发中" name="in_dev" />
      <el-tab-pane label="已完成" name="done" />
    </el-tabs>

    <div class="req-cards">
      <el-card v-for="req in requirements" :key="req.id" shadow="hover" class="req-card" @click="$router.push(`/requirements/${req.id}`)">
        <div class="req-header">
          <span class="req-no">{{ req.req_no }}</span>
          <PriorityTag :priority="req.priority" />
          <StatusBadge :status="req.status" type="requirement" />
        </div>
        <h3 class="req-title">{{ req.title }}</h3>
        <p class="req-desc">{{ req.description?.slice(0, 80) }}...</p>
        <div class="req-footer">
          <span>提出人: {{ getNickname(req.proposer_id) }}</span>
          <span v-if="req.expected_date">预计: {{ req.expected_date }}</span>
          <el-progress :percentage="calcProgress(req)" :stroke-width="8" style="width: 120px" />
        </div>
      </el-card>
    </div>

    <el-empty v-if="requirements.length === 0" description="暂无需求" />

    <!-- Create Dialog -->
    <el-dialog v-model="showCreateDialog" title="新建需求" width="600px" @close="resetForm">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题" required><el-input v-model="form.title" placeholder="需求标题" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" :rows="4" placeholder="需求描述" /></el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="form.priority" style="width: 100%">
            <el-option label="🔴 高" value="high" /><el-option label="🟡 中" value="medium" /><el-option label="🟢 低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="预计上线"><el-date-picker v-model="form.expected_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { getRequirementsApi, createRequirementApi } from '@/api/requirement'
import { mockUsers } from '@/mock/data'
import PriorityTag from '@/components/PriorityTag.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import { ElMessage } from 'element-plus'

const requirements = ref<any[]>([])
const search = ref('')
const activeFilter = ref('all')
const showCreateDialog = ref(false)

const form = reactive({ title: '', description: '', priority: 'medium', expected_date: '' })

const getNickname = (id: string) => mockUsers.find((u) => u.id === id)?.nickname || '未知'
const calcProgress = (req: any) => {
  if (!req.children?.length) return 0
  return Math.round((req.children.filter((c: any) => c.status === 'done').length / req.children.length) * 100)
}

const loadRequirements = async () => {
  requirements.value = await getRequirementsApi({ status: activeFilter.value, search: search.value }) as any[]
}

const handleCreate = async () => {
  if (!form.title) { ElMessage.warning('请填写标题'); return }
  await createRequirementApi({ ...form, status: 'draft', proposer_id: '1' })
  ElMessage.success('创建成功')
  showCreateDialog.value = false
  loadRequirements()
}

const resetForm = () => { Object.assign(form, { title: '', description: '', priority: 'medium', expected_date: '' }) }

onMounted(loadRequirements)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { margin: 0; }
.header-actions { display: flex; gap: 12px; }
.req-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 16px; margin-top: 16px; }
.req-card { cursor: pointer; transition: transform 0.2s; }
.req-card:hover { transform: translateY(-2px); }
.req-header { display: flex; gap: 8px; align-items: center; margin-bottom: 8px; }
.req-no { font-weight: 600; color: #409EFF; font-size: 13px; }
.req-title { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
.req-desc { color: #909399; font-size: 13px; line-height: 1.5; }
.req-footer { display: flex; align-items: center; gap: 16px; margin-top: 12px; font-size: 12px; color: #909399; }
</style>
