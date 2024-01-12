<template lang="pug">
.card.align-items-center.p-3
    img.card-image.card-img-top(:src="image" alt="cardImage")
    .card-body
        h5.card-title.text-opacity-75.fw-bold {{ title }}
        p.card-text.text-muted {{ text }}
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: "ContentCard",
    props: {
        title: String,
        text: String,
        image: String,
        imageStyle: String
    }
})
</script>

<style scoped lang="scss">
@import '@/styles/styles.scss';

.card-image {
    height: 16rem;
    width: 19rem;
}

.card {
    transition: transform 0.3s ease-in-out;
    border: 1px solid $almost-non-existent-grey !important;

    &:hover {
        transform: scale(1.02);
    }

    &:not(:hover) {
        transition: transform 0.5s ease-in-out;
    }
}
</style>
