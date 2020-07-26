import inflect
from fractions import Fraction

p = inflect.engine()
from math import *


def linguistic_ratio(ratio, *, allow_times=True, allow_integral_shorthand=True, prefix_half=False):
    halfstring = ("one " if prefix_half else "") + "half"
    if ratio < 0:
        return "negative" + linguistic_ratio(-ratio, allow_times=allow_times, allow_integral_shorthand=False,
                                             prefix_half=True)
    if ratio == 1:
        return ""
    elif ratio.numerator == 1:
        if ratio.denominator == 2:
            return halfstring
        else:
            return "one " + p.number_to_words(p.ordinal(ratio.denominator))
    elif ratio.denominator == 1:
        if ratio.numerator == 2 and allow_integral_shorthand:
            return "twice"
        else:
            return p.number_to_words(ratio.numerator) + (" times" if allow_times else "")
    else:
        if ratio > 1:
            integral = floor(ratio)
            sub = ratio - integral
            return p.number_to_words(integral) + " and " + \
                   linguistic_ratio(sub, allow_times=False,
                                    allow_integral_shorthand=allow_integral_shorthand,
                                    prefix_half=True) + (" times" if allow_times else "")
        else:
            if ratio.denominator == 2:
                return p.number_to_words(ratio.numerator) + " halves"
            else:
                return p.number_to_words(ratio.numerator) + " " + p.plural(
                    p.number_to_words(p.ordinal(ratio.denominator)))


def latex_fraction(fraction, oneblank=False):
    if fraction.denominator == 1:
        if fraction.numerator == 1 and oneblank:
            return ""
        return str(fraction.numerator)
    return complex_latex_fraction(str(fraction.numerator), str(fraction.denominator))


def complex_latex_fraction(a, b):
    return r"\frac{" + a + "}{" + b + "}"
