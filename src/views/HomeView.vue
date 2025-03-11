<template>
  <Sidebar/>

  <div>
    <h1>Hello, World!</h1>
    <p>Welcome to the Home Page.</p>

  </div>

</template>

<script>

import Sidebar from "@/components/Sidebar.vue";
export default {
  name: 'HomePage',
  components: {Sidebar},
};


</script>

<style scoped>
/* 首页特有的样式 */
h1 {
  color: #42b983;
}
</style>
