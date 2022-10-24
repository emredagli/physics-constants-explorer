def get_symbol(key, power):
    if power == 0:
        return ""
    elif power == 1:
        return key
    else:
        return key + "^" + str(power)


def get_power_range(max_power):
    return list(range(-max_power, max_power + 1))


power_map = str.maketrans({
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"})


def get_explanation(current, number, power):
    multiplication_str = "." if current else ""

    if power == 1:
        return current + multiplication_str + str(number)

    return current + multiplication_str + str(number) + str(power).translate(power_map)


def get_formatted_symbol(symbol):
    multiplication_symbol = " ⋅ "  # or " ✕ " ?
    pairs = symbol.strip().split()
    numerator = []
    denominator = []
    for pair in pairs:
        value_pair = pair.split('^')
        if len(value_pair) == 2:
            power = int(value_pair[1])
            if power < 0:
                if power == -1:
                    denominator.append(value_pair[0])
                else:
                    denominator.append(value_pair[0] + str(abs(power)).translate(power_map))
            else:
                numerator.append(value_pair[0] + str(value_pair[1]).translate(power_map))
        else:
            numerator.append(value_pair[0])

    formatted_numerator = "1"
    if len(numerator) > 0:
        formatted_numerator = multiplication_symbol.join(numerator)

    if len(denominator) > 0:
        formatted_denominator = multiplication_symbol.join(denominator)
        if len(denominator) == 1:
            formatted = f"{formatted_numerator} / {formatted_denominator}"
        else:
            formatted = f"{formatted_numerator} / ({formatted_denominator})"
    else:
        formatted = formatted_numerator

    return formatted
