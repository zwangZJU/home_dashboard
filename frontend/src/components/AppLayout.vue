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
        background-color="#001529"
        text-color="#ffffffb3"
        active-text-color="#409EFF"
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
  background-color: #001529;
  transition: width 0.3s;
  overflow: hidden;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #ffffff1a;
}
.logo-text {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  white-space: nowrap;
}
.sidebar-menu {
  border-right: none;
}
.sidebar-menu:not(.el-menu--collapse) {
  width: 220px;
}
.header {
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  z-index: 10;
}
.collapse-btn {
  cursor: pointer;
  margin-right: 16px;
  color: #606266;
}
.collapse-btn:hover {
  color: #409EFF;
}
.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}
.header-right {
  margin-left: auto;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #606266;
}
.username {
  font-size: 14px;
}
.main-content {
  background: #f5f7fa;
  overflow-y: auto;
}
</style>
