<template>
  <div class="login-container">
    <div class="bg-orbs">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>
    <div class="login-card">
      <h1 class="login-title">📊 DevTrack</h1>
      <p class="login-subtitle">开发项目全流程展示系统</p>
      <el-tabs v-model="activeTab" class="cyber-tabs">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" @submit.prevent="handleLogin">
            <el-form-item>
              <el-input v-model="loginForm.username" prefix-icon="User" placeholder="用户名" size="large" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="loginForm.password" prefix-icon="Lock" type="password" placeholder="密码" size="large" show-password />
            </el-form-item>
            <el-button type="primary" size="large" :loading="loading" class="login-btn" @click="handleLogin">登 录</el-button>
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
            <el-button type="primary" size="large" class="login-btn" @click="handleRegister">注 册</el-button>
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
  background: linear-gradient(135deg, #0b1120 0%, #1a0533 50%, #0b1120 100%);
  position: relative;
  overflow: hidden;
}

/* Animated background orbs */
.bg-orbs {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;
}
.orb-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #00f0ff, transparent 70%);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}
.orb-2 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #7c3aed, transparent 70%);
  bottom: -80px;
  right: -80px;
  animation-delay: -7s;
}
.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #06b6d4, transparent 70%);
  top: 50%;
  left: 60%;
  animation-delay: -14s;
}
@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(40px, -30px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(30px, 40px) scale(1.02); }
}

.login-card {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 240, 255, 0.15);
  border-radius: 16px;
  padding: 40px;
  width: 420px;
  box-shadow: 0 0 40px rgba(0, 240, 255, 0.08), 0 25px 50px rgba(0, 0, 0, 0.4);
  position: relative;
  z-index: 1;
}
.login-title {
  text-align: center;
  font-size: 28px;
  font-family: 'Orbitron', sans-serif;
  background: linear-gradient(135deg, #00f0ff, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}
.login-subtitle {
  text-align: center;
  color: #94a3b8;
  margin-bottom: 24px;
}
.login-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  letter-spacing: 4px;
}
.demo-hint {
  text-align: center;
  margin-top: 16px;
}
</style>
