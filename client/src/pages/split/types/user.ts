export class User {
    constructor(
        public id: Number,
        public email: String,
        public firstName: String,
        public lastName: String,
        public currency: String,
        public avatar?: String | undefined) {}

    static toJson(user: User | undefined) {
        return JSON.stringify({
            pk: user?.id,
            email: user?.email,
            first_name: user?.firstName,
            last_name: user?.lastName,
            currency: user?.currency,
            avatar: user?.avatar
        })
    }

    static copyWith(base: User, changes: Partial<User>): User {
            return new User(
                changes.id !== undefined ? changes.id : base.id,
                changes.email !== undefined ? changes.email : base.email,
                changes.firstName !== undefined ? changes.firstName : base.firstName,
                changes.lastName !== undefined ? changes.lastName : base.lastName,
                changes.currency !== undefined ? changes.currency : base.currency,
                changes.avatar !== undefined ? changes.avatar : base.avatar,
            );
        }

    getFullName() {
        return `${this.firstName} ${this.lastName}`
    }
}