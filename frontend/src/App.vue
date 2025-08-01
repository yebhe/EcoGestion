
<template>
  <div>
    <NavBar />
    <div class="routes">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue';
</script>


<style scoped>
.routes {
  padding-top: 70px; 
}
</style>