from decimal import ROUND_HALF_UP, Decimal


def euro(value: str | int | Decimal) -> Decimal:
    """Converte in Decimal arrotondando al centesimo."""
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
