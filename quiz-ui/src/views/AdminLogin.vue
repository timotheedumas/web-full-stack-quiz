<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const password = ref('');
const errorMessage = ref('');
const router = useRouter();

async function login() {
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/login`, {
      password: password.value,
    });

    if (response.status === 200 && response.data.token) {
      localStorage.setItem('isAdmin', 'true');
      localStorage.setItem('adminToken', response.data.token); // ✅ token JWT stocké
      router.push('/admin/questions');
    }
  } catch {
    errorMessage.value = 'Mauvais mot de passe';
  }
}
</script>

<template>
  <div class="container mt-5" style="max-width: 400px">
    <h1 class="mb-4 text-center">Connexion admin</h1>

    <input
      type="password"
      class="form-control mb-3"
      placeholder="Mot de passe"
      v-model="password"
    />

    <button class="btn btn-primary w-100" @click="login">Connexion</button>

    <div class="text-danger mt-3 text-center" v-if="errorMessage">
      {{ errorMessage }}
    </div>
  </div>
</template>
