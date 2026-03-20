// Mock users
export const mockUsers = [
  { id: '1', username: 'zhaozhao', nickname: '昭昭', email: 'zz@example.com', avatar_url: '', role: 'admin' },
  { id: '2', username: 'qiuqiu', nickname: '球球', email: 'qq@example.com', avatar_url: '', role: 'member' },
  { id: '3', username: 'xiaotuan', nickname: '小团', email: 'xt@example.com', avatar_url: '', role: 'member' },
]

// Mock requirements
export const mockRequirements = [
  {
    id: '1', req_no: 'REQ-001', title: '用户登录功能',
    description: '支持账号密码登录、第三方OAuth登录，包括微信和Google登录方式。',
    priority: 'high', status: 'in_dev', proposer_id: '1',
    expected_date: '2026-04-01', parent_id: null,
    created_at: '2026-03-15 10:00:00', updated_at: '2026-03-18 14:00:00',
    children: [
      { id: '1-1', title: '账号密码登录', status: 'done', assignee: '小团' },
      { id: '1-2', title: 'OAuth 2.0 接入', status: 'done', assignee: '球球' },
      { id: '1-3', title: '登录安全策略', status: 'in_progress', assignee: '球球' },
      { id: '1-4', title: '登录日志记录', status: 'todo', assignee: '小团' },
    ],
    history: [
      { time: '2026-03-18 14:00', operator: '昭昭', action: '状态从"待评审"改为"已通过"' },
      { time: '2026-03-15 10:00', operator: '昭昭', action: '创建了此需求' },
    ],
  },
  {
    id: '2', req_no: 'REQ-002', title: '数据导出功能',
    description: '支持将任务和需求数据导出为 Excel 和 CSV 格式。',
    priority: 'medium', status: 'review', proposer_id: '2',
    expected_date: '2026-04-10', parent_id: null,
    created_at: '2026-03-18 09:00:00', updated_at: '2026-03-20 11:00:00',
    children: [
      { id: '2-1', title: 'Excel 导出', status: 'todo', assignee: '小团' },
      { id: '2-2', title: 'CSV 导出', status: 'todo', assignee: '球球' },
    ],
    history: [
      { time: '2026-03-18 09:00', operator: '球球', action: '创建了此需求' },
    ],
  },
  {
    id: '3', req_no: 'REQ-003', title: '任务看板拖拽',
    description: '实现任务看板的拖拽排序功能，支持跨列拖拽。',
    priority: 'high', status: 'done', proposer_id: '1',
    expected_date: '2026-03-25', parent_id: null,
    created_at: '2026-03-12 14:00:00', updated_at: '2026-03-20 16:00:00',
    children: [
      { id: '3-1', title: 'vuedraggable 集成', status: 'done', assignee: '小团' },
      { id: '3-2', title: '拖拽状态同步', status: 'done', assignee: '球球' },
    ],
    history: [
      { time: '2026-03-20 16:00', operator: '昭昭', action: '标记为已完成' },
      { time: '2026-03-12 14:00', operator: '昭昭', action: '创建了此需求' },
    ],
  },
  {
    id: '4', req_no: 'REQ-004', title: '通知系统',
    description: '实现站内通知功能，任务状态变更、截止提醒等。',
    priority: 'low', status: 'draft', proposer_id: '3',
    expected_date: '2026-04-15', parent_id: null,
    created_at: '2026-03-20 15:00:00', updated_at: '2026-03-20 15:00:00',
    children: [],
    history: [
      { time: '2026-03-20 15:00', operator: '小团', action: '创建了此需求' },
    ],
  },
  {
    id: '5', req_no: 'REQ-005', title: '权限管理优化',
    description: '细粒度权限控制，支持项目级别的角色配置。',
    priority: 'medium', status: 'approved', proposer_id: '1',
    expected_date: '2026-04-20', parent_id: null,
    created_at: '2026-03-19 10:00:00', updated_at: '2026-03-20 09:00:00',
    children: [],
    history: [],
  },
  {
    id: '6', req_no: 'REQ-006', title: '移动端适配',
    description: '响应式布局优化，确保在移动设备上可用。',
    priority: 'medium', status: 'draft', proposer_id: '1',
    expected_date: null, parent_id: null,
    created_at: '2026-03-20 17:00:00', updated_at: '2026-03-20 17:00:00',
    children: [],
    history: [],
  },
]

// Mock tasks
export const mockTasks = [
  { id: '1', task_no: 'TASK-001', title: '首页UI设计', description: '设计仪表盘首页布局和视觉方案', status: 'done', priority: 'low', assignee_id: '3', requirement_id: '3', due_date: '2026-03-20', estimated_hours: 8, subtasks: [{ id: 's1', title: '线框图', is_done: true }, { id: 's2', title: '视觉稿', is_done: true }], comments: [{ id: 'c1', user_id: '3', content: '设计稿已完成', created_at: '2026-03-19 16:00' }] },
  { id: '2', task_no: 'TASK-002', title: '用户注册功能', description: '实现用户注册接口和页面', status: 'testing', priority: 'medium', assignee_id: '3', requirement_id: '1', due_date: '2026-03-22', estimated_hours: 12, subtasks: [{ id: 's3', title: '注册API', is_done: true }, { id: 's4', title: '注册页面', is_done: true }], comments: [] },
  { id: '3', task_no: 'TASK-003', title: 'OAuth 2.0 接入', description: '集成微信和Google OAuth登录', status: 'in_progress', priority: 'high', assignee_id: '2', requirement_id: '1', due_date: '2026-03-25', estimated_hours: 16, subtasks: [{ id: 's5', title: '搭建OAuth服务端', is_done: true }, { id: 's6', title: '接入微信/Google', is_done: false }, { id: 's7', title: 'Token刷新机制', is_done: false }], comments: [{ id: 'c2', user_id: '2', content: '微信接入需要申请', created_at: '2026-03-20 11:00' }] },
  { id: '4', task_no: 'TASK-004', title: '登录安全策略', description: '实现登录限流、密码强度检查等', status: 'in_progress', priority: 'high', assignee_id: '2', requirement_id: '1', due_date: '2026-03-28', estimated_hours: 10, subtasks: [], comments: [] },
  { id: '5', task_no: 'TASK-005', title: '登录日志记录', description: '记录用户登录日志用于审计', status: 'todo', priority: 'medium', assignee_id: '3', requirement_id: '1', due_date: '2026-03-28', estimated_hours: 6, subtasks: [], comments: [] },
  { id: '6', task_no: 'TASK-006', title: 'Excel导出功能', description: '实现数据导出为Excel', status: 'todo', priority: 'medium', assignee_id: '3', requirement_id: '2', due_date: '2026-04-05', estimated_hours: 8, subtasks: [], comments: [] },
  { id: '7', task_no: 'TASK-007', title: 'CSV导出功能', description: '实现数据导出为CSV', status: 'todo', priority: 'low', assignee_id: '2', requirement_id: '2', due_date: '2026-04-08', estimated_hours: 4, subtasks: [], comments: [] },
  { id: '8', task_no: 'TASK-008', title: '数据库设计', description: '设计核心数据表结构', status: 'done', priority: 'high', assignee_id: '2', requirement_id: null, due_date: '2026-03-18', estimated_hours: 8, subtasks: [], comments: [] },
]

// Mock meetings
export const mockMeetings = [
  {
    id: '1', title: '需求评审会', meeting_type: 'review',
    meeting_time: '2026-03-20 14:00', duration_minutes: 90,
    host_id: '1', participants: ['1', '2', '3'],
    content: '## 讨论内容\n1. 讨论 DevTrack 系统的整体需求\n2. 确定五个核心模块的优先级\n3. 球球建议使用 PostgreSQL + FastAPI\n4. 小团建议前端用 Vue3 + TailwindCSS',
    created_at: '2026-03-20 16:00',
    decisions: [
      { id: 'd1', content: '确定技术栈: FastAPI + Vue3 + PostgreSQL', is_resolved: true },
      { id: 'd2', content: 'MVP 周期定为 2 周（待确认）', is_resolved: false },
      { id: 'd3', content: '后续接入 AI 辅助（待评估）', is_resolved: false },
    ],
    related_tasks: ['TASK-008'],
    notes: ['球球: 建议先做任务看板，这是核心体验', '小团: 看板拖拽需要用 vuedraggable'],
  },
  {
    id: '2', title: '周会', meeting_type: 'weekly',
    meeting_time: '2026-03-18 10:00', duration_minutes: 60,
    host_id: '1', participants: ['1', '2', '3'],
    content: '## 本周进展\n- 球球：完成数据库设计，开始认证模块\n- 小团：完成前端项目搭建，开始登录页面\n\n## 下周计划\n- 完成认证模块联调\n- 开始需求管理模块',
    created_at: '2026-03-18 11:30',
    decisions: [
      { id: 'd4', content: '认证模块本周完成', is_resolved: true },
    ],
    related_tasks: [],
    notes: ['昭昭: 下周三做一次代码Review'],
  },
  {
    id: '3', title: '每日站会', meeting_type: 'daily',
    meeting_time: '2026-03-19 09:30', duration_minutes: 15,
    host_id: '1', participants: ['1', '2', '3'],
    content: '## 进展同步\n- 各模块正常推进中',
    created_at: '2026-03-19 10:00',
    decisions: [],
    related_tasks: [],
    notes: [],
  },
]

// Dashboard stats
export const mockDashboardStats = {
  total_requirements: 24,
  active_tasks: 12,
  completed_tasks: 8,
  overdue_tasks: 2,
}

export const mockTrendData = [
  { date: '03-01', count: 1 }, { date: '03-03', count: 2 }, { date: '03-05', count: 1 },
  { date: '03-07', count: 3 }, { date: '03-09', count: 2 }, { date: '03-11', count: 4 },
  { date: '03-13', count: 1 }, { date: '03-15', count: 3 }, { date: '03-17', count: 2 },
  { date: '03-19', count: 5 }, { date: '03-20', count: 3 },
]
