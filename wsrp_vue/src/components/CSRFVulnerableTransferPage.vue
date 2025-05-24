<template>
  <NavBar />
  <main class="transfer-container">
    <div class="form-header">
      <h2>Transfer Money</h2>
    </div>
    <CSRFVulnerableForm />
    <div class="button-container">
      <button class="back-button" @click="handleBack">
        Back to Dashboard
      </button>
    </div>
  </main>
</template>

<script setup>
import CSRFVulnerableForm from "./CSRFVulnerableForm.vue";
import NavBar from "./NavBar.vue";
import { useRouter } from 'vue-router';

const router = useRouter();

const handleBack = () => {
  router.push('/dashboard');
};
</script>

<style scoped>
.transfer-container {
  max-width: 800px;
  margin: 80px auto 0;
  padding: 2rem;
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.button-container {
  margin-top: 2rem;
  text-align: center;
}

.back-button {
  background: none;
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  color: var(--bank-gold);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.75rem 1.5rem;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: rgba(207, 181, 59, 0.1);
  color: var(--bank-gold-light);
  transform: translateY(-2px);
}

h2 {
  color: var(--bank-gold);
  margin: 0;
  font-size: 1.8rem;
}
</style> 