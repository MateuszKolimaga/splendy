import { useToasts } from "./useToasts";

const { addToast } = useToasts()
export const loginTrigger = (to: { query: { verification: any; invitation: any }; }, _: any, next: () => void) => {
    const verification = to.query.verification;
    if (verification === "1") {
      addToast({ message: 'Email is verified', type: 'success'})
    }
    next();
  }