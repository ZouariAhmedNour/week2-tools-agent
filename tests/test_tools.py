import pytest

from src.tools import calculator, convert_currency, add_tax


def test_calculator_addition():
    assert calculator("10 + 5") == 15.0


def test_calculator_priority():
    assert calculator("10 + 5 * 2") == 20.0


def test_calculator_division():
    assert calculator("20 / 4") == 5.0


def test_convert_usd_to_tnd():
    assert convert_currency(25, "USD", "TND") == 77.5


def test_convert_same_currency():
    assert convert_currency(50, "TND", "TND") == 50.0


def test_convert_unsupported_currency():
    with pytest.raises(ValueError):
        convert_currency(50, "GBP", "TND")


def test_add_tax():
    assert add_tax(100, 19) == 119.0


def test_add_tax_negative_rate():
    with pytest.raises(ValueError):
        add_tax(100, -5)


def test_calculator_blocks_unsafe_expression():
    with pytest.raises(ValueError):
        calculator("__import__('os').system('dir')")