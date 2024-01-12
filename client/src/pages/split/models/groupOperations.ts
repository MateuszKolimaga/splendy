export default class GroupOperation {
    constructor(
        public from_user: number,
        public team: number,
        public currency: string,
        public to_users: number[] = [],
        public users_settled: number[] = [],
        public description?: string,
        public date?: Date,
        public value?: number,
        public attachments?: unknown[],
        public id?: number,
    ) {
        if (!to_users) {
            this.to_users = [from_user];
        }
        this.users_settled = [from_user];
    }
}