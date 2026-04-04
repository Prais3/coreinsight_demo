from src.algorithms import find_duplicates, is_prime, flatten_nested

def test_find_duplicates():
    assert find_duplicates([1, 2, 2, 3, 3]) == [2, 3]
    assert find_duplicates([1, 2, 3]) == []

def test_is_prime():
    assert is_prime(7) is True
    assert is_prime(9) is False
    assert is_prime(1) is False

def test_flatten_nested():
    assert flatten_nested([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]