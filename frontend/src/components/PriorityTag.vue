<template>
  <el-tag :type="tagType" size="small" effect="dark" round>
    <span class="mr-1">{{ emoji }}</span> {{ label }}
  </el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ priority: string }>()

const map: Record<string, [string, string, string]> = {
  high: ['danger', '🔴', '高'],
  medium: ['warning', '🟡', '中'],
  low: ['success', '🟢', '低'],
}
const [tagType, emoji, label] = computed(() => map[props.priority] || map.low).value
</script>
