import { readonly, ref } from "vue";

export type ToastData = {
    id: number
    type?: "success" | "info" | "warning" | "danger"
    message?: string
    duration?: number
    dismiss: () => void
    stacking?: boolean
    position?: "start" | "end" | "center"
}

type ToastsData = Array<ToastData>

export type ToastOptions = Omit<ToastData, "id" | "dismiss">

const state = ref<ToastsData>([]);

const defaultOptions: ToastOptions = {
    type: "info",
    position: "center",
    message: "",
    stacking: true,
    duration: 5000
};

const dismiss = (id: number) => {
    state.value = state.value.filter((t) => t.id !== id);
};

const addToast = (options: ToastOptions = defaultOptions): ToastData => {
    const id = Math.floor(Math.random() * Date.now());

    const toast: ToastData = {
        ...defaultOptions, ...options,
        id,
        dismiss: () => dismiss(id)
    };
    if (!toast.stacking) {
        state.value = state.value.filter((t) => t.position !== options.position);
    }
    if (toast.position?.includes("top")) {
        state.value = [toast, ...state.value];
    } else {
        state.value.push(toast);
    }

    return toast;
};

const useToasts = () => {
    return {
        toasts: readonly(state),
        addToast,
        dismiss
    };
};
export { useToasts };