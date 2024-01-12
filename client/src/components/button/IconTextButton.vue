<template lang="pug">
.icon-text-button
   font-awesome-icon(icon=`${icon || "plus"}`)
   | {{ text }}

</template>
  
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
name: "IconTextButton",
props: {
    icon: {
        type: String,
        required: true,
    },
    text: {
        type: String,
        required: true,
    },
}
});
</script>

<style scoped>
.icon-text-button {
    display: flex;
    flex-direction: row;
    padding: 0.2rem;
    align-items: center;
    justify-items: center;
    gap: 0.2rem;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out;
}
</style>