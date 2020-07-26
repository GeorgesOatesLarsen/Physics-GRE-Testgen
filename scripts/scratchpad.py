import sys

# This is so we can find gregen from this script.
from fractions import Fraction

sys.path.append('.')
import gregen as gg
import gregen.mathhelpers as mh
import gregen.linguistichelpers as lh
import random

print("Generating your test, bossman!")
A = mh.friendly_ratio(1)
B = mh.friendly_ratio(1)
C = A * B
lp = mh.similar_fractions(C, 5, True)
print(C)
print(lp)
