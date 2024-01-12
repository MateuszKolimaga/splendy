export function anyKeysOfObject(
    keys: (string | number | symbol)[],
    obj: object
): boolean {
    for (var key of keys) {
        if (key in obj) return true
    }
    return false
}
