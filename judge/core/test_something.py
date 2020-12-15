import pytest

from time import sleep

from random import randint


def test_something():
    for i in range(100):
        assert isinstance(i, int), 'it should be a string'
        #sleep(randint(1, 3))
