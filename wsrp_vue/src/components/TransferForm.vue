<template>
  <div class="transfer-form">
    <div class="user-info">
      <p class="user-type">{{ props.userProfile.user.user_type }}</p>
      <p class="user-name">{{ props.userProfile.user.first_name }} {{ props.userProfile.user.last_name }}</p>
    </div>

    <form @submit="submitTransfer">
      <div class="form-group">
        <label for="fromAccount">From Account</label>
        <select v-model="fromAccount" id="fromAccount" required>
          <option v-for="account in userAccounts" :key="account.account_id" :value="account.account_id">
            {{ account.account_number }} ({{ account.account_type }}) - ${{ account.account_balance }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="toAccount">To Account</label>
        <select v-model="toAccount" id="toAccount" required>
          <option v-for="account in allAccounts" :key="account.account_id" :value="account.account_id">
            {{ account.account_number }} ({{ account.account_type }}) - ${{ account.account_balance }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="amount">Amount</label>
        <input
          v-model="amount"
          type="number"
          id="amount"
          min="0.01"
          step="0.01"
          required
        />
      </div>

      <div v-if="error" class="error">{{ error }}</div>

      <button type="submit">Transfer Money</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  userProfile: {
    type: Object,
    required: true,
  },
});

const router = useRouter();
const fromAccount = ref('');
const toAccount = ref('');
const amount = ref('');
const error = ref('');
const userAccounts = ref([]);
const allAccounts = ref([]);

const fetchUserAccounts = async () => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/accounts?user_id=${props.userProfile.user.user_id}`,
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
      }
    );
    if (response.ok) {
      const data = await response.json();
      userAccounts.value = data.accounts;
    }
  } catch (err) {
    error.value = 'Error fetching accounts';
    console.error(err);
  }
};

const fetchAllAccounts = async () => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/accounts`,
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
      }
    );
    if (response.ok) {
      const data = await response.json();
      allAccounts.value = data.accounts;
    }
  } catch (err) {
    error.value = 'Error fetching all accounts';
    console.error(err);
  }
};

const submitTransfer = async (event) => {
  event.preventDefault();
  error.value = '';

  if (fromAccount.value === toAccount.value) {
    error.value = 'Cannot transfer to the same account';
    return;
  }

  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/csrf_vuln/transfer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from_account: fromAccount.value,
        to_account: toAccount.value,
        amount: parseFloat(amount.value)
      })
    });

    if (response.ok) {
      router.push('/dashboard');
    } else {
      const data = await response.json();
      error.value = data.message || 'Transfer failed';
    }
  } catch (err) {
    error.value = 'Error processing transfer';
    console.error(err);
  }
};

onMounted(() => {
  fetchUserAccounts();
  fetchAllAccounts();
});
</script>

<style scoped>
.transfer-form {
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
}

.user-info {
  margin-bottom: 2rem;
  text-align: center;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(207, 181, 59, 0.2);
}

.user-type {
  color: var(--bank-gold);
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
}

.user-name {
  color: var(--bank-white);
  font-size: 1.3rem;
  font-weight: 500;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  color: var(--bank-gold);
  margin-bottom: 0.5rem;
}

select, input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--bank-white);
}

button {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, var(--bank-gold) 0%, var(--bank-gold-dark) 100%);
  border: none;
  border-radius: 8px;
  color: var(--bank-blue-dark);
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(207, 181, 59, 0.3);
}

.error {
  color: #ff4444;
  margin-bottom: 1rem;
  text-align: center;
}
</style> 