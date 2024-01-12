<template lang="pug">
.date-wrapper
    | {{ month }}
    .day-wrapper {{ day }}
    .hour-wrapper {{ hour }}
</template>

<script lang="ts">
import { PropType, defineComponent } from 'vue';

export default defineComponent({
    name: "DateComponent",
    props: {
        date: {
            type: [String, Date] as PropType<string | Date>,
            required: true
        }
    },
    setup(props) {
        let date: Date;
        if (typeof props.date === 'string') {
            date = new Date(props.date);
        } else {
            date = props.date!;
        }
        return {
            month: date.toLocaleString('default', { month: 'short' }),
            day: date.getDate(),
            hour: date.toTimeString().split(' ')[0].slice(0, -3)
        }
    }
})
</script>

<style lang="scss">
.date-wrapper {
    display: flex;
    flex-direction: column;
    text-transform: uppercase;
    justify-content: center;
    align-items: center;
    text-align: center;
    max-width: 1.5rem;
}

.day-wrapper {
    margin-top: -0.5rem;
    font-size: x-large;
    text-align: center;
    width: inherit;
}
.hour-wrapper {
    margin-top: -0.5rem;
    margin-right: -0.2rem;
    font-size: x-small;
    text-align: center;
    width: inherit;
}
</style>
