import sys

# This is so we can find gregen from this script.
from fractions import Fraction

sys.path.append('.')
import gregen as gg
import gregen.mathhelpers as mh
import gregen.linguistichelpers as lh
import random

print("Generating your test, bossman!")
with open('output.tex', 'w') as file:
    file.write(gg.generatetest(generatorset=gg.ProblemSet(gg.generators.ETS2017.AllProblems), nquestions=10))