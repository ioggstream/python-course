def float_to_decimal_base(q, precision=24, base=2):
    """
    Convert a finite, rational number in binary format.

    The algorithm is explicit and for didactic purposes only. It is not efficient.
    """
    f = float(q)
    b = ""

    i = int(f)
    d = f - i

    # Represent an integer in base n.
    # We start from the least significant digit
    # and work our way up to the most significant digit.
    # 13(base 10) = 1 * 2^0 + 0 * 2^1 + 1*2^2 + 1*2^3 = 1101(base 2)
    while True:
        r = i % base
        b = str(r) + b
        i = i - r
        if i == 0:
            break
        i = int(i / base)

    b += "."

    # Represent a fraction in base n.
    # We start from the most significant digit
    # and work our way down to the least significant digit.
    # 0.625 = 1 * 2^-1 + 0 * 2^-2 + 1 * 2^-3 = 0.101(base 2)
    for _ in range(precision):
        d = d * base
        # Common block between this and the integer case.
        i = int(
            d
        )  # Integer part is analogous to the modulo operation of the integer case.
        b = b + str(i)
        d = d - i
        if d == 0:
            break
    return b
