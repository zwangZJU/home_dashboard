import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { noAuth: true },
    },
    {
      path: '/',
      component: () => import('@/components/AppLayout.vue'),
      redirect: '/dashboard',
      children: [
        { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard.vue'), meta: { title: '仪表盘' } },
        { path: 'requirements', name: 'Requirements', component: () => import('@/views/requirements/RequirementList.vue'), meta: { title: '需求管理' } },
        { path: 'requirements/:id', name: 'RequirementDetail', component: () => import('@/views/requirements/RequirementDetail.vue'), meta: { title: '需求详情' } },
        { path: 'tasks', name: 'Tasks', component: () => import('@/views/tasks/TaskBoard.vue'), meta: { title: '任务管理' } },
        { path: 'meetings', name: 'Meetings', component: () => import('@/views/meetings/MeetingList.vue'), meta: { title: '会议纪要' } },
        { path: 'meetings/:id', name: 'MeetingDetail', component: () => import('@/views/meetings/MeetingDetail.vue'), meta: { title: '会议详情' } },
        { path: 'progress', name: 'Progress', component: () => import('@/views/progress/ProgressView.vue'), meta: { title: '进度展示' } },
        { path: 'admin', name: 'Admin', component: () => import('@/views/admin/AdminPanel.vue'), meta: { title: '系统管理' } },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (!to.meta.noAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
