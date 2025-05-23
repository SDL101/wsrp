<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const user_name = ref("");
const password = ref("");
const scriptContainerVisible = ref(false);
const scriptText1 = ref("");
const scriptText2 = ref("");
const scriptCount = ref(0);
const bruteForceSuccess = ref(false);
const loginError = ref(false);

// close response container when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.response-container')) {
    scriptContainerVisible.value = false;
  }
});

async function loadWordlist(file) {
      const res = await fetch(file);
      const lines = await res.text();
      return lines.trim().split('\n').map(l => l.trim()).filter(Boolean);
    }

const bruteForceLogin = async () => {
    const usernames = await loadWordlist('/common_usernames.txt');
    const passwords = await loadWordlist('/common_pws.txt');
    let attempts = 0;

    scriptContainerVisible.value = true;
    scriptText1.value = "Starting brute force attack...";

    for (const user of usernames) {
        for (const pass of passwords) {
            attempts++;

            scriptCount.value = attempts;

            const res = await fetch( `${import.meta.env.VITE_API_URL}/api/brute_force_vuln/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_name: user, password: pass })
            });

            if (res.ok) {
                const data = await res.json();
                bruteForceSuccess.value = true;
                if (data.access_token) {
                    scriptText2.value = `Success! Username: ${user}, Password: ${pass}`;
                    console.log(`Success! Username: ${user}, Password: ${pass}`);
                    console.log(`Total Attempts: ${attempts}`);
                    return;
                }
            }
        }
    }
}

const login = async () => {
  const endpoint = "/api/auth/login";
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_name: user_name.value,
      password: password.value,
    }),
  };

  const response = await fetch(`${import.meta.env.VITE_API_URL}${endpoint}`, options);
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    // Store the access token in local storage
    localStorage.setItem("access_token", data.access_token);
    // Redirect to the Customer Dashboard
    router.push("/dashboard");
  } else {
    // Handle login error
    console.error("Login failed");
    // show login error in the form
    loginError.value = true;
  }
};
</script>

<template>
  <div class="container">
    <div class="item">
      <h2 class="login-title">Brute Force Vulnerable Login</h2>
      <form @submit.prevent="login">
        <label for="username">Username</label>
        <input v-model="user_name" type="text" placeholder="Username" />
        <label for="password">Password</label>
        <input v-model="password" type="password" placeholder="Password" />
        <p v-if="loginError" class="login-error">Login failed. Please try again.</p>
        <button type="submit">Login</button>
        <p>
          Don't have an account?
          <router-link to="/register">Register</router-link>
        </p>
        <p>Want to try to guess?</p>
        
      </form>
      <button @click="bruteForceLogin">Brute Force It</button>
    </div>

    <!-- Response Container  -->
    <div v-if="scriptContainerVisible" class="response-container">
      <span class="response-container-header">
        <h3>Brute Force Status</h3>
        <button id="close-response" @click="scriptContainerVisible = false; bruteForceSuccess = false">Close</button>
      </span>
      <pre>{{ scriptText1 }}</pre>
      <pre>Current iteration: {{ scriptCount }}</pre>
      <div v-if="bruteForceSuccess">
        <pre >{{ scriptText2 }}</pre>
        <pre>Now close this window and try to log in with the retrieved credentials.</pre>
      </div>
      
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Align items to the left */
  margin-top: 2rem;
}

.item {
  display: flex;
  flex-direction: column;
  position: relative;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
  width: 100%; /* Ensure it takes full width */
}

.login-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--bank-gold);
  text-align: center;
}

.instructions {
  margin-top: 1.5rem;
  width: 100%; /* Ensure it takes full width */
  background: rgba(255, 255, 255, 0.1); /* Light background for contrast */
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 1.5rem; /* Add padding for better spacing */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

.instructions-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--bank-gold);
  margin-bottom: 1rem;
}

.instructions-description {
  font-size: 1.1rem;
  color: var(--bank-white);
  margin-bottom: 1rem;
}

.instructions-steps {
  margin-left: 1.5rem; /* Indent the list */
  color: var(--bank-white);
}

.instructions-warning {
  margin-top: 1rem;
  font-weight: 600;
  color: var(--bank-red); /* Use a contrasting color for warnings */
}

.toggle-button {
  background: var(--bank-gold);
  color: var(--bank-blue-dark);
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.toggle-button:hover {
  background: var(--bank-gold-dark);
}

.instructions-content {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
}

input {
  display: block;
  width: 100%;
  margin: 1rem 0;
  padding: 1rem;
  font-size: 1.1rem;
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--bank-white);
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--bank-gold);
}

button {
  margin: 1.5rem 0;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  background: linear-gradient(
    135deg,
    var(--bank-gold) 0%,
    var(--bank-gold-dark) 100%
  );
  color: var(--bank-blue-dark);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  width: 100%;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(207, 181, 59, 0.4);
  background: linear-gradient(
    135deg,
    var(--bank-gold-light) 0%,
    var(--bank-gold) 100%
  );
}

.error-message {
  color: #f44336;
  font-size: 1rem;
  margin-top: 0.5rem;
  text-align: center;
}

.response-container{
  position: absolute;
  z-index: 1000;
  bottom: 5%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #000000CC;
  padding: 1rem;
  padding-top: 0;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 1000px;
  max-width: 1200px;
}
.response-container-header{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
button#close-response{
  top: 10px;
  right: 10px;
  background: linear-gradient( 135deg, var(--bank-gold) 0%, var(--bank-gold-dark) 100% );;
  border: none;
  color: #fff;
  cursor: pointer;
  width:fit-content;
  transition: color 0.3s ease;
}
.response-container h3{
  color: #fff;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}
.response-container h4{
  color: #fff;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}
.response-container pre{
  text-wrap: wrap;
  white-space: pre-line;
  word-wrap: break-word;
}

.login-error{
  color: red;
}
</style>
