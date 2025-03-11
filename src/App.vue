<!-- App.vue -->
<template>
  <!-- 如果不需要导航栏等全局组件，直接渲染路由视图 -->
  <router-view />
</template>

<script>
export default {
  name: "App"
}
</script>

<style>
/* 全局样式 */
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

#app {
  height: 100vh;
  display: flex;
}
</style>