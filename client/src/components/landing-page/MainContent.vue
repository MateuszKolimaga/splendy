<template lang="pug">
.content(@mousemove="handleMouseMove")
  .row.mt-3
    .col-md-6.d-flex.flex-row.align-items-center.justify-content-center
      .text-content.text-left.d-flex.flex-column
        h1
          strong Managing your finances has never been
          span.easier.ms-1(style="cursor: pointer") easier
        p Try our web app completely for free, forever.
        .div
          button.btn.btn-lg.btn-primary(@click="login") Start Free
          //- button.btn.btn-lg.btn-outline-secondary.ms-2(@click="showDemo") Show demo
    .col-md-6.d-flex.flex-row.align-items-center.justify-content-center
      .visual-content.d-flex.flex-column.justify-content-center
        floating-svg-component(v-if="!isSmallScreen" ref="imageRef")
        img.main-image(v-else :src="images.people" alt="Image")

</template>

<script lang="ts">
import { defineComponent, onBeforeUnmount, onMounted, ref } from 'vue'
import people from '../../assets/people.svg'
import FloatingSvgComponent from './FloatingSvgComponent.vue'

export default defineComponent({
    name: 'MainContent',
    components: {
        FloatingSvgComponent,
    },
    setup() {
        const imageRef = ref(null)
        const isSmallScreen = ref(window.innerWidth < 1200)

        const handleResize = () => {
            isSmallScreen.value = window.innerWidth < 1200
        }

        onMounted(() => {
            window.addEventListener('resize', handleResize)
        })

        onBeforeUnmount(() => {
            window.removeEventListener('resize', handleResize)
        })

        return {
            imageRef,
            isSmallScreen,
        }
    },
    data() {
        return {
            images: {
                people,
            },
        }
    },
    methods: {
        handleMouseMove(event: any) {
            if (!this.isSmallScreen) {
                //@ts-ignore
                this.imageRef!.handleMouseMove(event)
            }
        },
        login() {
            this.$router.push('/login')
        },
    },
})
</script>

<style lang="scss" scoped>
@import '@/styles/styles.scss';

.content {
    background: $green-gradient-background;
    display: flex;
    justify-content: center;
    padding-top: 6%;
    padding-bottom: 4%;

    @media (max-width: $md) {
        flex-direction: column;
    }

    @media (max-width: $sm) {
        padding-top: 6rem;
    }
}

.main-image {
    height: 480px;
    width: 585px;

    @media (max-width: $md) {
        height: 330px;
        width: 470px;
    }

    @media (max-width: $sm) {
        height: 300px;
        width: 420px;
        margin-top: 2rem;
    }

    @media (max-width: $xs) {
        height: 19rem;
        width: 22rem;
    }
}

h1,
p {
    @media (max-width: $xs) {
        text-align: center;
    }
}

.easier {
    text-decoration: underline;
    text-decoration-color: #ffe779;
    font-style: italic;
    font-weight: bold;
}

.text-content {
    @media (min-width: $md) {
        padding-left: 4rem !important;
    }

    @media (min-width: $sm) {
        padding-left: 2rem;
    }

    @media (max-width: $sm) {
        text-align: center;
        margin-top: 3rem;
        padding-inline: 5rem;
    }

    h1,
    a {
        @media (max-width: $sm) {
            align-self: center;
        }
    }

    @media (max-width: $xs) {
        text-align: center;
        margin-top: 1rem;
    }
}
</style>
