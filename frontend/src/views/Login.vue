<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">📊 DevTrack</h1>
      <p class="login-subtitle">开发项目全流程展示系统</p>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" @submit.prevent="handleLogin">
            <el-form-item>
              <el-input v-model="loginForm.username" prefix-icon="User" placeholder="用户名" size="large" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="loginForm.password" prefix-icon="Lock" type="password" placeholder="密码" size="large" show-password />
            </el-form-item>
            <el-button type="primary" size="large" :loading="loading" style="width: 100%" @click="handleLogin">登 录</el-button>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="register">
          <el-form :model="registerForm" @submit.prevent="handleRegister">
            <el-form-item>
              <el-input v-model="registerForm.username" prefix-icon="User" placeholder="用户名" size="large" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="registerForm.email" prefix-icon="Message" placeholder="邮箱" size="large" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="registerForm.password" prefix-icon="Lock" type="password" placeholder="密码" size="large" show-password />
            </el-form-item>
            <el-button type="primary" size="large" style="width: 100%" @click="handleRegister">注 册</el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <div class="demo-hint">
        <el-text type="info" size="small">演示账号: zhaozhao / qiuqiu / xiaotuan （密码任意）</el-text>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const activeTab = ref('login')
const loading = ref(false)

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ username: '', email: '', password: '' })

const handleLogin = async () => {
  if (!loginForm.username) { ElMessage.warning('请输入用户名'); return }
  loading.value = true
  try {
    await userStore.login(loginForm.username, loginForm.password)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch {
    ElMessage.error('登录失败')
  } finally {
    loading.value = false
  }
}

const handleRegister = () => {
  ElMessage.info('注册功能暂未对接后端')
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  width: 420px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}
.login-title {
  text-align: center;
  font-size: 28px;
  color: #303133;
  margin-bottom: 8px;
}
.login-subtitle {
  text-align: center;
  color: #909399;
  margin-bottom: 24px;
}
.demo-hint {
  text-align: center;
  margin-top: 16px;
}
</style>
