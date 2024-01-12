export interface Debt {
    value: number,
    currency: string,
}

export class Member {
    constructor(
        public id: Number,
        public email: String,
        public firstName: String,
        public lastName: String,
        public currency: String,
        public avatar?: String | undefined,
        public youOwe?: Debt | undefined,
        public owesYou?: Debt | undefined) {}

    static toJson(user: Member | undefined) {
        return JSON.stringify({
            pk: user?.id,
            email: user?.email,
            first_name: user?.firstName,
            last_name: user?.lastName,
            currency: user?.currency,
            avatar: user?.avatar,
            youOwe: user?.youOwe,
            owesYou: user?.owesYou
        })
    }

    static copyWith(base: Member, changes: Partial<Member>): Member {
        return new Member(
            changes.id !== undefined ? changes.id : base.id,
            changes.email !== undefined ? changes.email : base.email,
            changes.firstName !== undefined ? changes.firstName : base.firstName,
            changes.lastName !== undefined ? changes.lastName : base.lastName,
            changes.currency !== undefined ? changes.currency : base.currency,
            changes.avatar !== undefined ? changes.avatar : base.avatar,
            changes.youOwe !== undefined ? changes.youOwe : base.youOwe,
            changes.owesYou !== undefined ? changes.owesYou : base.owesYou,
        );
    }
}