<script setup>
import { ref } from 'vue';

defineProps({
  question: Object,
});

const emit = defineEmits(['click-on-answer']);
const activeIndex = ref(null);

// Tableau de classes couleurs à appliquer dans l'ordre
const colorClasses = ['button-red', 'button-blue', 'button-yellow', 'button-green'];
</script>

<template>
  <div class="mt-4 text-center">
    <h2 class="mb-3">{{ question.title }}</h2>
    <p class="mb-4">{{ question.text }}</p>

    <img
      v-if="question.image"
      :src="question.image"
      alt="Image de la question"
      class="img-fluid mb-4"
      style="max-height: 300px"
    />

    <div class="container">
      <div class="row justify-content-center">
        <div
          v-for="(answer, index) in question.possibleAnswers"
          :key="answer.id"
          class="col-md-6 mb-3"
        >
          <button
            class="btn w-100 py-3 text-uppercase fw-bold"
            :class="[
              colorClasses[index] || 'btn-secondary',
              { 'pulse-click': activeIndex === index },
            ]"
            @click="
              () => {
                activeIndex = index;
                emit('click-on-answer', answer.id);
                setTimeout(() => (activeIndex = null), 300);
              }
            "
          >
            {{ answer.text }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
