export function useDateFormatter() {
    function formatDateTime(date: Date) {
      const options = {
        day: "numeric" as const,
        month: "numeric" as const,
        year: "numeric" as const,
        hour: "numeric" as const,
        minute: "numeric" as const,
      };
  
      return new Intl.DateTimeFormat("en-GB", options).format(date);
    }
  
    return {
      formatDateTime,
    };
  }