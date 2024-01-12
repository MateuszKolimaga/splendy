declare module "vue-css-donut-chart";
declare module 'vue3-resize';
declare module '*.svg' {
    import Vue, {VueConstructor} from 'vue';
    const content: VueConstructor<Vue>;
    export default content;
  }