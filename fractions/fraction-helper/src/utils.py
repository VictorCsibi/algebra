def add_fractions(num1, den1, num2, den2):
    common_denominator = den1 * den2
    new_num1 = num1 * den2
    new_num2 = num2 * den1
    result_num = new_num1 + new_num2
    return simplify_fraction(result_num, common_denominator)

def subtract_fractions(num1, den1, num2, den2):
    common_denominator = den1 * den2
    new_num1 = num1 * den2
    new_num2 = num2 * den1
    result_num = new_num1 - new_num2
    return simplify_fraction(result_num, common_denominator)

def multiply_fractions(num1, den1, num2, den2):
    result_num = num1 * num2
    result_den = den1 * den2
    return simplify_fraction(result_num, result_den)

def divide_fractions(num1, den1, num2, den2):
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    result_num = num1 * den2
    result_den = den1 * num2
    return simplify_fraction(result_num, result_den)

def simplify_fraction(num, den):
    gcd = greatest_common_divisor(num, den)
    return num // gcd, den // gcd

def greatest_common_divisor(a, b):
    while b:
        a, b = b, a % b
    return abs(a)