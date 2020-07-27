import random
from fractions import Fraction
from pylatex import *

from ...base import ProblemGenerator
from ...base import ProblemGeneratorGroup
from ...base import ProblemSet
from ... import mathhelpers as mh
from ... import linguistichelpers as lh
import math


class Group(ProblemGeneratorGroup):
    category = "Fundamental Kinematics"

    @staticmethod
    def getallweighted(set):
        return [
            ProblemSet.weigh(ETS17P1, 1),
            ProblemSet.weigh(ETS17P3, 1)
        ]


class ETS17P1(ProblemGenerator):
    category = Group.category
    name = "ETS17P1"
    origin = "ETS17"

    @staticmethod
    def generate(nanswers):
        ratio_A = mh.friendly_ratio(1)
        ratio_B = mh.friendly_ratio(1)
        answer_ratio = 1

        find = random.choice(["force", "accel", "mass"])
        force_ratio = None
        mass_ratio = None
        accel_ratio = None
        swap_force = random.choice([True, False])
        swap_mass = random.choice([True, False])
        swap_accel = random.choice([True, False])

        if find == "force":
            mass_ratio = ratio_A
            accel_ratio = ratio_B
            answer_ratio = mass_ratio * accel_ratio
            identa = "F_A"
            identb = "F_B"

        if find == "accel":
            mass_ratio = ratio_A
            force_ratio = ratio_B
            answer_ratio = force_ratio / mass_ratio
            identa = "a_A"
            identb = "a_B"

        if find == "mass":
            accel_ratio = ratio_A
            force_ratio = ratio_B
            answer_ratio = force_ratio / accel_ratio
            identa = "m_A"
            identb = "m_B"

        answer_ratios, tcn = mh.similar_fractions_centered(answer_ratio, nanswers, seeda=ratio_A, seedb=ratio_B)
        sorted_answer_ratios, correctn = mh.sort_rational_answers(answer_ratios, tcn)

        statement = r"A net force $F_A$ acts on object $A$ and a net force $F_B$ acts on object $B$. "
        if mass_ratio != None:
            if (swap_mass):
                statement += "The mass of object $A$ is " + lh.linguistic_ratio(
                    1 / mass_ratio) + " the mass of object $B$. "
            else:
                statement += "The mass of object $B$ is " + lh.linguistic_ratio(
                    mass_ratio) + " the mass of object $A$. "
        if force_ratio != None:
            if (swap_force):
                statement += "$F_A$ is " + lh.linguistic_ratio(1 / force_ratio) + " $F_B$. "
            else:
                statement += "$F_B$ is " + lh.linguistic_ratio(force_ratio) + " $F_A$. "
        if accel_ratio != None:
            if (swap_accel):
                statement += "The acceleration of object $A$ is " + lh.linguistic_ratio(
                    1 / accel_ratio) + " that of object $B$. "
            else:
                statement += "The acceleration of object $B$ is " + lh.linguistic_ratio(
                    accel_ratio) + " that of object $A$. "
        if find == "force":
            statement += "Which of the following is true of forces $" + identa + "$ and $" + identb + "$?"
        if find == "accel":
            statement += "Which of the following is true of the accelerations of $A$ and $B$, $" + identa + "$ and $" + identb + "$?"
        if find == "mass":
            statement += "Which of the following is true of the masses of $A$ and $B$, $" + identa + "$ and $" + identb + "$?"
        answers = []
        bfirst = random.choice([True, False])
        for ratio in sorted_answer_ratios:
            if bfirst:
                answers.append(NoEscape(
                    r"$\displaystyle " + identb + " = " + lh.latex_fraction(ratio, oneblank=True) + identa + "$"))
            else:
                answers.append(NoEscape(
                    r"$\displaystyle " + identa + " = " + lh.latex_fraction(1 / ratio, oneblank=True) + identb + "$"))

        return {
            'statement': NoEscape(statement),
            'answers': answers,
            'correctn': correctn,
            'jumble': False
        }


class ETS17P3(ProblemGenerator):
    category = Group.category
    name = "ETS17P3"
    origin = "ETS17"

    @staticmethod
    def generate(nanswers):
        ratio_Lsqrt = mh.friendly_ratio(1)
        ratio_Gsqrt = mh.friendly_ratio(1)
        ratio_L = ratio_Lsqrt ** 2
        ratio_G = ratio_Gsqrt ** 2
        ratio_T = ratio_Lsqrt / ratio_Gsqrt
        ratio_M = mh.friendly_ratio(1)
        if random.choice([True, False]):
            ratio_M = Fraction(1, 1)

        answer_ratio = Fraction(1, 1)

        find = random.choice(["L", "G", "T"])
        swap_L = random.choice([True, False])
        swap_G = random.choice([True, False])
        swap_T = random.choice([True, False])
        periodidents = [r"\omega", "f", "T"]
        periodmode = random.randint(0, 2)

        if (periodmode != 2):
            ratio_T = 1 / ratio_T

        seeda = seedb = None
        if find == "G":
            seeda = ratio_L
            seedb = ratio_T
            answer_ratio = ratio_G
            ratio_G = None
            identa = "g_A"
            identb = "g_B"

        if find == "L":
            seeda = ratio_G
            seedb = ratio_T
            answer_ratio = ratio_L
            ratio_L = None
            identa = "L_A"
            identb = "L_B"

        if find == "T":
            seeda = ratio_L
            seedb = ratio_G
            answer_ratio = ratio_T
            ratio_T = None
            identa = periodidents[periodmode] + "_A"
            identb = periodidents[periodmode] + "_B"

        answer_ratios, tcn = mh.similar_fractions_centered(answer_ratio, nanswers, seeda=seeda, seedb=seedb)
        sorted_answer_ratios, correctn = mh.sort_rational_answers(answer_ratios, tcn)

        statement = "Two simple pendulums $A$ and $B$ consist of " + (
            "identical masses" if ratio_M == 1 else "masses $m_A$ and $m_B$") \
                    + " suspended from strings of " + (
                        "identical length." if ratio_L == 1 else " lengths $L_A$ and $L_B$ respectively.") + " "
        if ratio_G != None:
            if (ratio_G == 1):
                statement += "The two pendulums oscillate in equal gravitational fields."
            elif (swap_G):
                statement += "The gravitational field in which $A$ oscillates is " + lh.linguistic_ratio(
                    1 / ratio_G) + " that of $B$. "
            else:
                statement += "The gravitational field in which $B$ oscillates is " + lh.linguistic_ratio(
                    ratio_G) + " that of $A$. "
        if ratio_T != None:
            if (ratio_G == 1):
                if (periodmode == 0):
                    statement += "The two pendulums oscillate at an identical angular frequency. "
                if (periodmode == 1):
                    statement += "The two pendulums oscillate at an identical frequency. "
                if (periodmode == 2):
                    statement += "The two pendulums have identical period. "
            else:
                first = "$B$"
                last = "$A$"
                finalratio = ratio_T
                if (swap_T):
                    last = "$B$"
                    first = "$A$"
                    finalratio = 1 / ratio_T
                if (periodmode == 0):
                    statement += "The angular frequency of pendulum " + first + " is " + lh.linguistic_ratio(
                        finalratio) + " that of " + last + ". "
                if (periodmode == 1):
                    statement += "The frequency of pendulum " + first + " is " + lh.linguistic_ratio(
                        finalratio) + " that of " + last + ". "
                if (periodmode == 2):
                    statement += "The period of pendulum " + first + " is " + lh.linguistic_ratio(
                        finalratio) + " that of " + last + ". "
        if ratio_L != None:
            if (ratio_L == 1):
                pass
            elif (swap_L):
                statement += "The length of pendulum A is " + lh.linguistic_ratio(1 / ratio_L) + " that of B. "
            else:
                statement += "The length of pendulum B is " + lh.linguistic_ratio(ratio_L) + " that of A. "

        if find == "L":
            statement += "Which of the following is true of pendulum lengths $" + identa + "$ and $" + identb + "$?"
        if find == "G":
            statement += "Which of the following is true of the gravitational accelerations of $A$ and $B$, $" + identa + "$ and $" + identb + "$ respectively?"
        if find == "T":
            statement += "Which of the following is true of the pendulum " + \
                         ["angular frequencies", "frequencies", "periods"][periodmode]
            statement += " of $A$ and $B$, $" + identa + "$ and $" + identb + "$ respectively?"
        answers = []
        bfirst = random.choice([True, False])
        for ratio in sorted_answer_ratios:
            if bfirst:
                answers.append(NoEscape(
                    r"$\displaystyle " + identb + " = " + lh.latex_fraction(ratio, oneblank=True) + identa + "$"))
            else:
                answers.append(NoEscape(
                    r"$\displaystyle " + identa + " = " + lh.latex_fraction(1 / ratio, oneblank=True) + identb + "$"))

        return {
            'statement': NoEscape(statement),
            'answers': answers,
            'correctn': correctn,
            'jumble': False
        }
