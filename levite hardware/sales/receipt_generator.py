def generate_receipt(sale_items):
    """
    sale_items: list of dicts with keys:
        - description (str)
        - quantity (int)
        - amount (float)
    Returns a formatted receipt string.
    """
    lines = []
    lines.append("RECEIPT".center(32))
    lines.append("-" * 32)
    lines.append("{:<14}{:>4}{:>12}".format("DESCRIPTION", "", "AMOUNT"))
    lines.append("")

    total = 0.0
    for item in sale_items:
        desc = item["description"]
        qty = item["quantity"]
        amt = item["amount"]
        lines.append("{:<10}{:>6}{:>12,.2f}".format(desc, qty, amt))
        total += amt

    lines.append("")
    lines.append("-" * 32)
    lines.append("{:<14}{:>16.2f}".format("TOTAL", total))
    lines.append("")
    lines.append("THANK YOU".center(32))

    return "\n".join(lines)
