<template>
  <div class="task-board-page">
    <div class="page-header">
      <h2>✅ 任务管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true"><el-icon><Plus /></el-icon> 新建任务</el-button>
      </div>
    </div>

    <div class="board">
      <div v-for="col in columns" :key="col.key" class="board-column">
        <div class="column-header">
          <span class="column-title">{{ col.label }}</span>
          <el-badge :value="getTasksByStatus(col.key).length" type="info" />
        </div>
        <draggable
          :list="getTasksByStatus(col.key)"
          :group="{ name: 'tasks' }"
          item-key="id"
          class="column-body"
          ghost-class="ghost"
          @end="onDragEnd"
        >
          <template #item="{ element }">
            <div class="task-card" @click="openDetail(element)">
              <div class="task-card-header">
                <span class="task-no">{{ element.task_no }}</span>
                <PriorityTag :priority="element.priority" />
              </div>
              <div class="task-card-title">{{ element.title }}</div>
              <div class="task-card-meta">
                <el-avatar :size="24">{{ getNickname(element.assignee_id)?.[0] || '?' }}</el-avatar>
                <span class="task-assignee">{{ getNickname(element.assignee_id) }}</span>
              </div>
              <div class="task-card-footer">
                <el-progress
                  v-if="element.subtasks?.length"
                  :percentage="Math.round(element.subtasks.filter((s: any) => s.is_done).length / element.subtasks.length * 100)"
                  :stroke-width="6"
                  :show-text="false"
                  style="flex: 1"
                />
                <span class="task-due" :class="{ overdue: isOverdue(element.due_date) }">
                  📅 {{ element.due_date }}
                </span>
              </div>
            </div>
          </template>
        </draggable>
      </div>
    </div>

    <!-- Task Detail Drawer -->
    <el-drawer v-model="showDetail" :title="`${selectedTask?.task_no} · ${selectedTask?.title}`" size="480px">
      <div v-if="selectedTask" class="task-detail">
        <el-form label-position="top">
          <el-form-item label="状态">
            <el-select :model-value="selectedTask.status" @change="updateStatus" style="width: 100%">
              <el-option v-for="s in statusOptions" :key="s.value" :label="s.label" :value="s.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="优先级">
            <el-select :model-value="selectedTask.priority" style="width: 100%">
              <el-option label="🔴 高" value="high" /><el-option label="🟡 中" value="medium" /><el-option label="🟢 低" value="low" />
            </el-select>
          </el-form-item>
          <el-form-item label="负责人">{{ getNickname(selectedTask.assignee_id) }}</el-form-item>
          <el-form-item label="截止日期">{{ selectedTask.due_date || '未设置' }}</el-form-item>
          <el-form-item label="预估工时">{{ selectedTask.estimated_hours ? selectedTask.estimated_hours + 'h' : '未设置' }}</el-form-item>
          <el-form-item label="描述"><div class="task-desc">{{ selectedTask.description }}</div></el-form-item>
        </el-form>

        <el-divider>子任务</el-divider>
        <div class="subtask-list">
          <div v-for="st in selectedTask.subtasks" :key="st.id" class="subtask-item">
            <el-checkbox v-model="st.is_done" />
            <span :class="{ done: st.is_done }">{{ st.title }}</span>
          </div>
          <el-empty v-if="!selectedTask.subtasks?.length" description="暂无子任务" :image-size="40" />
        </div>

        <el-divider>评论</el-divider>
        <div class="comment-list">
          <div v-for="c in selectedTask.comments" :key="c.id" class="comment-item">
            <strong>{{ getNickname(c.user_id) }}</strong>
            <span class="comment-time">{{ c.created_at }}</span>
            <p>{{ c.content }}</p>
          </div>
        </div>
        <div class="comment-input">
          <el-input v-model="newComment" placeholder="输入评论..." @keyup.enter="addComment">
            <template #append><el-button @click="addComment">发送</el-button></template>
          </el-input>
        </div>
      </div>
    </el-drawer>

    <!-- Create Dialog -->
    <el-dialog v-model="showCreateDialog" title="新建任务" width="520px">
      <el-form :model="createForm" label-width="80px">
        <el-form-item label="标题" required><el-input v-model="createForm.title" placeholder="任务标题" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="createForm.description" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="createForm.priority" style="width: 100%">
            <el-option label="🔴 高" value="high" /><el-option label="🟡 中" value="medium" /><el-option label="🟢 低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="截止日期"><el-date-picker v-model="createForm.due_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" /></el-form-item>
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
import draggable from 'vuedraggable'
import { getTasksApi, createTaskApi } from '@/api/task'
import { mockUsers } from '@/mock/data'
import PriorityTag from '@/components/PriorityTag.vue'
import { ElMessage } from 'element-plus'

const tasks = ref<any[]>([])
const showDetail = ref(false)
const showCreateDialog = ref(false)
const selectedTask = ref<any>(null)
const newComment = ref('')

const statusOptions = [
  { value: 'todo', label: '待办' }, { value: 'in_progress', label: '进行中' },
  { value: 'testing', label: '测试中' }, { value: 'done', label: '已完成' },
]

const columns = [
  { key: 'todo', label: '📋 待办' },
  { key: 'in_progress', label: '🔧 进行中' },
  { key: 'testing', label: '🧪 测试中' },
  { key: 'done', label: '✅ 已完成' },
]

const getNickname = (id: string) => mockUsers.find((u) => u.id === id)?.nickname || '未知'
const getTasksByStatus = (status: string) => tasks.value.filter((t) => t.status === status)
const isOverdue = (date: string) => date && date < new Date().toISOString().split('T')[0]

const openDetail = (task: any) => { selectedTask.value = task; showDetail.value = true }

const updateStatus = async (status: string) => {
  if (selectedTask.value) {
    selectedTask.value.status = status
    ElMessage.success('状态已更新')
  }
}

const addComment = () => {
  if (!newComment.value.trim()) return
  selectedTask.value?.comments.push({
    id: Date.now().toString(), user_id: '3', content: newComment.value, created_at: new Date().toLocaleString(),
  })
  newComment.value = ''
}

const onDragEnd = () => {
  // Status is updated by the column assignment
  ElMessage.success('任务已移动')
}

const createForm = reactive({ title: '', description: '', priority: 'medium', due_date: '' })
const handleCreate = async () => {
  if (!createForm.title) { ElMessage.warning('请填写标题'); return }
  const newTask = await createTaskApi({ ...createForm, status: 'todo', assignee_id: '3', estimated_hours: 0 })
  tasks.value.push(newTask as any)
  showCreateDialog.value = false
  ElMessage.success('创建成功')
  Object.assign(createForm, { title: '', description: '', priority: 'medium', due_date: '' })
}

onMounted(async () => { tasks.value = await getTasksApi() })
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { margin: 0; }
.header-actions { display: flex; gap: 12px; }
.board { display: flex; gap: 16px; overflow-x: auto; padding-bottom: 16px; }
.board-column { flex: 1; min-width: 260px; background: #f0f2f5; border-radius: 12px; display: flex; flex-direction: column; max-height: calc(100vh - 180px); }
.column-header { padding: 12px 16px; display: flex; align-items: center; gap: 8px; }
.column-title { font-weight: 600; font-size: 15px; }
.column-body { flex: 1; overflow-y: auto; padding: 0 12px 12px; min-height: 60px; }
.task-card { background: #fff; border-radius: 10px; padding: 12px; margin-bottom: 8px; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.06); transition: transform 0.15s; }
.task-card:hover { transform: translateY(-1px); box-shadow: 0 3px 8px rgba(0,0,0,0.1); }
.ghost { opacity: 0.5; background: #e6f7ff; }
.task-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.task-no { font-size: 12px; color: #909399; font-weight: 600; }
.task-card-title { font-weight: 500; font-size: 14px; margin-bottom: 8px; }
.task-card-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.task-assignee { font-size: 12px; color: #606266; }
.task-card-footer { display: flex; align-items: center; gap: 8px; }
.task-due { font-size: 12px; color: #909399; white-space: nowrap; }
.task-due.overdue { color: #F56C6C; font-weight: 600; }
.task-desc { color: #606266; line-height: 1.6; white-space: pre-wrap; }
.subtask-list { display: flex; flex-direction: column; gap: 6px; }
.subtask-item { display: flex; align-items: center; gap: 8px; }
.subtask-item.done { text-decoration: line-through; color: #c0c4cc; }
.comment-list { display: flex; flex-direction: column; gap: 12px; margin-bottom: 12px; }
.comment-item strong { font-size: 13px; }
.comment-time { font-size: 12px; color: #c0c4cc; margin-left: 8px; }
.comment-item p { margin: 4px 0 0; color: #606266; font-size: 13px; }
.comment-input { margin-top: 8px; }
</style>
