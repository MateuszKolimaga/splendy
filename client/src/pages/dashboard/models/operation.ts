export class Operation {
    constructor(
        public user: string,
        public currency: string | undefined,
        public date?: Date | undefined,
        public value?: number | undefined,
        public description?: string | undefined,
        public category?: string | undefined,
    ) {}
}