<script setup>
import WelcomeBanner from "./WelcomeBanner.vue";
import LoginForm from "./LoginForm.vue";
import SQLVulnerableForm from "./SQLVulnerableForm.vue";
import XSSVulnerableForm from "./XSSVulnerableForm.vue";
import InstructionsCard from "./InstructionsCard.vue";
import NavBar from "./NavBar.vue";
import { useVulnerabilityStore } from "@/stores/vulnerabilityStore";
import BruteForceLogin from "./BruteForceLogin.vue";

const vulnerabilityStore = useVulnerabilityStore();
</script>

<template>
  <NavBar />
  <div class="wrapper">
    <WelcomeBanner msg="Gold Standard Bank" />

    <aside class="instructions-container">
      <InstructionsCard />
    </aside>
  </div>

  <main class="login-container">
    <XSSVulnerableForm v-if="vulnerabilityStore.getXssVulnerable()" />
    <SQLVulnerableForm v-else-if="vulnerabilityStore.getSqliVulnerable()" />
    <BruteForceLogin v-else-if="vulnerabilityStore.getBruteForceVulnerable()" />
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

.wrapper {
  margin-top: 100px; /* Increased to move WelcomeBanner further down */
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
