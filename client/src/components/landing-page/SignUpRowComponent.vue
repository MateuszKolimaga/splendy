<template lang="pug">
.portable-login-bg.w-100.container-fluid.py-3
    .d-flex.flex-row.justify-content-center.w-100
        .d-flex.flex-column.h-100
          portable-login-component
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import PortableLoginComponent from '@/components/landing-page/PortableLoginComponent.vue'

export default defineComponent({
  name: "SignUpRowComponent",
  components: {
    PortableLoginComponent
  },
  data() {
    var featureCardsContent = [
      "Scan your receipts", "Share expenses with up to 15 people", "Chat with your friends", 
      "Track your home budget", "Visualise your expenses and incomes",  "Use on the web and mobile"
    ]
    return {
      showCards: false,
      featureCardsContent,
    }
  },
  methods: {
    handleIntersection(entries: IntersectionObserverEntry[]) {
      const isVisible = entries[0].isIntersecting;
      if (isVisible) {
        this.showCards = true;
      }
    }
  },
  mounted() {
    const observer = new IntersectionObserver(this.handleIntersection);
    observer.observe(this.$el);
  }
});

</script>

<style scoped lang="scss">
@import "@/styles/styles.scss";
.portable-login-bg {
  background: $green-gradient-background-reverse;
}

.cards {
  @media(max-width: $md) {
    visibility: hidden;
  }
}

.feature-img {
  height: 5rem;
  width: 5rem;
  margin: 0 1rem 0 0.5rem;
}

.bg-card {
  // border: 2px solid #ffe67995 !important;
  // box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);

  &-even {
    border: 3px solid #7dc8bfa4 !important;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.feature-card {
  width: 90%;
  animation: fadeIn 0.8s ease-in forwards;
  opacity: 0; 
  // border: 2px solid #6dafa7;

  &:hover {
        transform: scale(1.02);
        // border: 1px solid black;
        // box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  &:not(:hover) {
      transition: transform 0.5s ease-in-out;
  }
}
</style>