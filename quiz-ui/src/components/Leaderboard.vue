<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
defineProps({
  scores: Array,
  highlight: String,
});
</script>
<template>
  <div>
    <ol class="list-group list-group-numbered">
      <li
        v-for="entry in scores"
        :key="entry.playerName + entry.date"
        class="list-group-item d-flex justify-content-between align-items-center"
        :class="{ 'list-group-item-info': highlight && entry.playerName === highlight }"
      >
        <span>{{ entry.playerName }}</span>
        <span>{{ entry.score }} pts</span>
      </li>
    </ol>
  </div>
</template>
