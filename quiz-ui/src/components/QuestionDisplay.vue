<script setup>
defineProps({
  question: Object,
});

const emit = defineEmits(['click-on-answer']);
</script>

<template>
  <div class="mt-4">
    <h2>{{ question.title }}</h2>
    <p>{{ question.text }}</p>

    <img v-if="question.image" :src="question.image" class="img-fluid mb-3" />

    <div class="list-group">
      <button
        v-for="answer in question.possibleAnswers"
        :key="answer.id"
        class="list-group-item list-group-item-action"
        @click="emit('click-on-answer', answer.id)"
      >
        {{ answer.text }}
      </button>
    </div>
  </div>
</template>
