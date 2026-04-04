def find_duplicates(items: list) -> list:
    """Return items that appear more than once."""
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                if items[i] not in duplicates:
                    duplicates.append(items[i])
    return duplicates


def is_prime(n: int) -> bool:
    """Check if n is prime."""
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def flatten_nested(nested: list) -> list:
    """Flatten an arbitrarily nested list."""
    result = []
    for item in nested:
        if isinstance(item, list):
            for subitem in flatten_nested(item):
                result.append(subitem)
        else:
            result.append(item)
    return result# trigger
