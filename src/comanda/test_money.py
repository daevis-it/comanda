from decimal import Decimal

from comanda.money import euro


def test_euro_arrotondamento():
    assert euro("12.345") == Decimal("12.35")


def test_float_error():
    assert 0.1 + 0.2 != 0.3  # Dimostrazione dell'errore di arrotondamento dei float
    assert euro(0.1) + euro(0.2) == euro(0.3)
