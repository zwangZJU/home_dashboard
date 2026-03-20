<template>
  <div class="admin-page">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="项目设置" name="project">
        <el-card shadow="hover">
          <el-form :model="projectForm" label-width="100px" style="max-width: 500px">
            <el-form-item label="项目名称"><el-input v-model="projectForm.name" /></el-form-item>
            <el-form-item label="项目描述"><el-input v-model="projectForm.description" type="textarea" :rows="3" /></el-form-item>
            <el-form-item label="项目状态">
              <el-select v-model="projectForm.status" style="width: 100%">
                <el-option label="进行中" value="active" /><el-option label="已归档" value="archived" />
              </el-select>
            </el-form-item>
            <el-form-item><el-button type="primary" @click="saveProject">保存</el-button></el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="成员管理" name="members">
        <el-card shadow="hover">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="card-title">👥 成员列表</span>
              <el-button type="primary" size="small"><el-icon><Plus /></el-icon> 邀请成员</el-button>
            </div>
          </template>
          <el-table :data="users" stripe>
            <el-table-column label="用户名" prop="username" />
            <el-table-column label="昵称" prop="nickname" />
            <el-table-column label="邮箱" prop="email" />
            <el-table-column label="角色">
              <template #default="{ row }">
                <el-tag :type="row.role === 'admin' ? 'danger' : 'info'" size="small">
                  {{ row.role === 'admin' ? '管理员' : '普通成员' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="160">
              <template #default="{ row }">
                <el-button text size="small" @click="toggleRole(row)">
                  {{ row.role === 'admin' ? '设为成员' : '设为管理员' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { mockUsers } from '@/mock/data'
import { ElMessage } from 'element-plus'

const activeTab = ref('project')
const users = ref<any[]>([])

const projectForm = reactive({ name: 'DevTrack', description: '开发项目全流程展示系统', status: 'active' })

const saveProject = () => { ElMessage.success('项目设置已保存') }
const toggleRole = (user: any) => {
  user.role = user.role === 'admin' ? 'member' : 'admin'
  ElMessage.success('角色已更新')
}

onMounted(() => { users.value = [...mockUsers] })
</script>

<style scoped>
.card-title { font-weight: 600; }
</style>
