<script setup>
import { onMounted } from "vue";
import Welcome from "./Welcome.vue";
import LoginForm from "./LoginForm.vue";
import SQLVulnerableForm from "./SQLVulnerableForm.vue";
import CSRFVulnerableForm from "./CSRFVulnerableForm.vue";
import XSSVulnerableForm from "./XSSVulnerableForm.vue";
import NavBar from "./NavBar.vue";
import { useRoute } from "vue-router";
import { useVulnerabilityStore } from "@/stores/vulnerabilityStore";

const route = useRoute();
const vulnerabilityStore = useVulnerabilityStore();
const isVulnerable = route.query.endpoint === "/api/sqli_vuln/auth/login";
const isCSRFEnabled = route.query.endpoint === "/api/csrf_vuln/transfer";
</script>

<template>
  <NavBar />
  <!-- <header> -->
  <div class="wrapper">
    <Welcome msg="Gold Standard Bank" />
  </div>
  <!-- </header> -->

  <main class="login-container">
    <XSSVulnerableForm v-if="vulnerabilityStore.getXssVulnerable()" />
    <SQLVulnerableForm v-else-if="vulnerabilityStore.getSqliVulnerable()" />
    <LoginForm v-else />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
  margin-top: 60px; /* Added to accommodate navbar */
  margin-bottom: 2rem;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.login-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
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
