def split_amount(amount: float, parts: int):
    split = round(amount / parts, 2)
    splits = [split] * (parts - 1)
    last_split = round(amount - sum(splits), 2)
    splits.append(last_split)
    return splits
