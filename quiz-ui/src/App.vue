<template>
  <div>
    <!-- 🔷 HEADER GLOBAL -->
    <header class="bg-light border-bottom p-3 d-flex justify-content-between">
      <router-link to="/" class="btn btn-outline-primary">🏠 Accueil</router-link>
      <router-link to="/admin/login" class="btn btn-outline-secondary">🔐 Admin</router-link>
    </header>

    <!-- 🧭 CONTENU DE LA PAGE COURANTE -->
    <router-view />
  </div>
</template>

<script setup></script>

<style scoped>
/* rien pour l’instant */
</style>
