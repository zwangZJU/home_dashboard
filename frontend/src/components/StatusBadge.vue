<template>
  <el-tag :type="tagType" size="small" effect="plain">{{ label }}</el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ status: string; type?: 'requirement' | 'task' }>()

const reqMap: Record<string, [string, string]> = {
  draft: ['info', '草稿'], review: ['warning', '待评审'], approved: ['success', '已通过'],
  in_dev: ['', '开发中'], done: ['success', '已完成'],
}
const taskMap: Record<string, [string, string]> = {
  todo: ['info', '待办'], in_progress: ['', '进行中'], testing: ['warning', '测试中'], done: ['success', '已完成'],
}

const source = computed(() => (props.type === 'requirement' ? reqMap : taskMap))
const [tagType, label] = computed(() => source.value[props.status] || ['info', props.status]).value
</script>
