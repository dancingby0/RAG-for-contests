<script setup lang="ts">
import {defineProps} from "vue";
import type {Communication} from "@/components/plain_objects/Communication";

const props = defineProps<{
  chatList: Communication[];
  selectedChat: number;
}>();

</script>

<template>

</template>

<style scoped>

</style>