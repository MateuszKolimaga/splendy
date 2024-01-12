export type Transfer = {
    id: Number,
    date: Date,
    fromUserId: Number
    toUserId: Number[] | Number
    value: Number,
    currency: String
}
