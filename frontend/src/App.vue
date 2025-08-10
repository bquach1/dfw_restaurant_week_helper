<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
</script>

<template>
  <div class="app-layout">
    <header>
      <img alt="Sushi" class="sushi" src="./assets/sushi.svg" width="125" height="125" />
      <div class="wrapper">
        <HelloWorld msg="DFW Restaurant Week Helper" />
      </div>
    </header>

    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  align-items: center;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

header {
  line-height: 1.5;
}

.sushi {
  display: block;
  margin: 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
