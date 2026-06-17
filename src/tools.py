import ast
import operator


SUPPORTED_RATES = {
    "USD_TND": 3.10,
    "EUR_TND": 3.35,
    "TND_USD": 1 / 3.10,
    "TND_EUR": 1 / 3.35,
}


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _safe_eval_node(node.left)
        right = _safe_eval_node(node.right)
        operator_type = type(node.op)

        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError("Opérateur non autorisé.")

        return _ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval_node(node.operand)
        operator_type = type(node.op)

        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError("Opérateur unaire non autorisé.")

        return _ALLOWED_OPERATORS[operator_type](operand)

    raise ValueError("Expression non autorisée.")


def calculator(expression: str) -> float:
    """
    Calcule une expression mathématique simple.

    Args:
        expression: Expression mathématique simple comme "10 + 5 * 2".

    Returns:
        Résultat numérique du calcul.
    """
    print(f"[TOOL CALL] calculator(expression={expression})")

    tree = ast.parse(expression, mode="eval")
    result = _safe_eval_node(tree.body)

    return round(float(result), 4)


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Convertit un montant entre deux devises avec des taux fixes pédagogiques.

    Args:
        amount: Montant à convertir.
        from_currency: Devise source, par exemple USD, EUR ou TND.
        to_currency: Devise cible, par exemple USD, EUR ou TND.

    Returns:
        Montant converti.
    """
    print(
        f"[TOOL CALL] convert_currency("
        f"amount={amount}, from_currency={from_currency}, to_currency={to_currency})"
    )

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == to_currency:
        return round(float(amount), 4)

    rate_key = f"{from_currency}_{to_currency}"

    if rate_key not in SUPPORTED_RATES:
        raise ValueError(
            f"Conversion non supportée : {from_currency} vers {to_currency}."
        )

    result = amount * SUPPORTED_RATES[rate_key]

    return round(float(result), 4)


def add_tax(amount: float, tax_rate: float) -> float:
    """
    Ajoute une taxe à un montant.

    Args:
        amount: Montant avant taxe.
        tax_rate: Taux de taxe en pourcentage, par exemple 19 pour 19%.

    Returns:
        Montant total après taxe.
    """
    print(f"[TOOL CALL] add_tax(amount={amount}, tax_rate={tax_rate})")

    if tax_rate < 0:
        raise ValueError("Le taux de taxe ne peut pas être négatif.")

    result = amount + (amount * tax_rate / 100)

    return round(float(result), 4)