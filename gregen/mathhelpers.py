from fractions import Fraction
import random
import sympy as sp
from sympy.core.symbol import S
import math


def friendly_ratio(complexity):
    n = friendly_integer(complexity)
    if random.choice([True, False]):
        return Fraction(1, n)
    else:
        return Fraction(n, 1)


def friendly_integer(complexity):
    friendly = 1
    for i in range(complexity):
        friendly *= random.choice([2, 3, 5, 7])
    return friendly


# Finds the smallest integer root of a fraction.
def smallest_root(fraction):
    factorization = sp.factorrat(S(fraction))
    powers = [v for k, v in factorization.items()]
    gcd = 1
    if len(powers) > 1:
        gcd = sp.igcd(*powers)
    if len(powers) == 1:
        gcd = abs(powers[0])
    result = Fraction(1, 1)
    for k, v in factorization.items():
        result *= Fraction(k, 1) ** int(v / gcd)
    return result, gcd


# Get some fractions that are similar to the given fraction
# The number of questions requested must always be odd for this to work well.
def similar_fractions_centered(answer, n, *, seeda=None, seedb=None, maxpow=2):
    fractions = [Fraction(1, 1)]
    ngen = int(math.floor(n / 2.0))

    if answer != 1:
        ngen -= 1
        tcn = 1
        fractions += [answer, 1 / answer]
    else:
        tcn = 0

    if ngen > 0:
        similars = similar_fractions(answer, ngen, seeda=seeda, seedb=seedb, minpow=1, maxpow=maxpow)
        for similar in similars:
            fractions.append(similar)
            fractions.append(1 / similar)

    return fractions, tcn


# Get some fractions that are similar to the given fraction.
def similar_fractions(answer, n, *, seeda=None, seedb=None, minpow=0, maxpow=2):
    if seeda is None:
        seeda = answer
    if seedb is None:
        seedb = answer
    factorizationa = sp.factorrat(S(seeda))
    factorizationb = sp.factorrat(S(seedb))
    allfactors = list(factorizationa.keys()) + list(factorizationb.keys())

    fractions = []
    for i in range(n):
        nf = Fraction(1, 1)
        for j in range(0, 10000):
            nf = Fraction(1, 1)
            for factor in allfactors:
                v = 1
                if factor not in factorizationb or (factor in factorizationa and random.choice([True, False])):
                    v = factorizationa[factor]
                else:
                    v = factorizationb[factor]
                nf *= Fraction(factor, 1) ** int(math.copysign(random.choice(range(minpow, maxpow + 1)), v))
            if nf not in fractions and nf != answer:
                break
        fractions.append(nf)
    return fractions


def sort_rational_answers(answers, correct):
    return sort_answers(answers, correct, lambda x: float(x.numerator) / x.denominator)


def sort_answers(answers, correct, key=lambda x: x):
    sa = sorted(enumerate(answers), key=lambda x: key(x[1]))
    ncorrect = 0
    for i, a in sa:
        if (i == correct):
            break
        ncorrect += 1
    return [a for i, a in sa], ncorrect
