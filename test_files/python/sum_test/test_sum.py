import operations


def test_sum_numbers():
    a = 1
    b = 2

    result = operations.sum_numbers(a, b)

    assert result == 3


def test_sum_negative_numbers():
    a = -1
    b = -2

    result = operations.sum_numbers(a, b)

    assert result == -3
