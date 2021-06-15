from django.test import TestCase


def add(x, y):
    """
    >>> add(6, 7)
    13
    >>> add(-2,7)
    5
    """
    return x + y


def subtract(x, y):
    """
    >>> subtract(6, 3)
    3
    """
    return x - y


def multiply(x, y):
    return x * y
