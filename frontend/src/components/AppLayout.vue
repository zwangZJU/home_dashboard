<template>
  <el-container class="app-layout">
    <el-aside :width="isCollapsed ? '64px' : '220px'" class="sidebar">
      <div class="logo">
        <span v-if="!isCollapsed" class="logo-text">📊 DevTrack</span>
        <span v-else class="logo-text">📊</span>
      </div>
      <el-menu
        :default-active="currentRoute"
        :collapse="isCollapsed"
        router
        class="sidebar-menu"
        background-color="#060d1b"
        text-color="#94a3b8"
        active-text-color="#00f0ff"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>
        <el-menu-item index="/requirements">
          <el-icon><Document /></el-icon>
          <template #title>需求管理</template>
        </el-menu-item>
        <el-menu-item index="/tasks">
          <el-icon><Tickets /></el-icon>
          <template #title>任务管理</template>
        </el-menu-item>
        <el-menu-item index="/meetings">
          <el-icon><ChatDotRound /></el-icon>
          <template #title>会议纪要</template>
        </el-menu-item>
        <el-menu-item index="/progress">
          <el-icon><TrendCharts /></el-icon>
          <template #title>进度展示</template>
        </el-menu-item>
        <el-menu-item index="/admin">
          <el-icon><Setting /></el-icon>
          <template #title>系统管理</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <el-icon class="collapse-btn" @click="isCollapsed = !isCollapsed" size="20">
          <Fold v-if="!isCollapsed" />
          <Expand v-else />
        </el-icon>
        <span class="page-title">{{ currentTitle }}</span>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <el-avatar :size="32">{{ userStore.userInfo?.nickname?.[0] || 'U' }}</el-avatar>
              <span class="username">{{ userStore.userInfo?.nickname || '用户' }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapsed = ref(false)

const currentRoute = computed(() => route.path)
const currentTitle = computed(() => (route.meta.title as string) || 'DevTrack')

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-layout {
  height: 100vh;
}
.sidebar {
  background-color: #060d1b;
  transition: width 0.3s;
  overflow: hidden;
  border-right: 1px solid rgba(0, 240, 255, 0.08);
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(0, 240, 255, 0.08);
}
.logo-text {
  font-family: 'Orbitron', sans-serif;
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, #00f0ff, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  white-space: nowrap;
}
.sidebar-menu {
  border-right: none !important;
}
.sidebar-menu:not(.el-menu--collapse) {
  width: 220px;
}
.sidebar-menu .el-menu-item {
  transition: all 0.3s ease;
  margin: 4px 8px;
  border-radius: 8px;
}
.sidebar-menu .el-menu-item:hover {
  background: rgba(0, 240, 255, 0.06) !important;
  box-shadow: 0 0 12px rgba(0, 240, 255, 0.05);
}
.sidebar-menu .el-menu-item.is-active {
  background: rgba(0, 240, 255, 0.1) !important;
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.1), inset 0 0 15px rgba(0, 240, 255, 0.05);
}
.header {
  background: rgba(11, 17, 32, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid rgba(0, 240, 255, 0.08);
  z-index: 10;
}
.collapse-btn {
  cursor: pointer;
  margin-right: 16px;
  color: #94a3b8;
  transition: all 0.3s ease;
}
.collapse-btn:hover {
  color: #00f0ff;
  text-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
}
.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #00f0ff;
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
}
.header-right {
  margin-left: auto;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #94a3b8;
  transition: color 0.3s ease;
}
.user-info:hover {
  color: #e2e8f0;
}
.username {
  font-size: 14px;
}
.main-content {
  background: #0b1120;
  overflow-y: auto;
}
</style>
