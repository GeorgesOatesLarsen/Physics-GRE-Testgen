import random
from fractions import Fraction
from pylatex import *

from ...base import ProblemGenerator
from ...base import ProblemGeneratorGroup
from ...base import ProblemSet
from ... import mathhelpers as mh
from ... import linguistichelpers as lh


class Group(ProblemGeneratorGroup):
    category = "Fundamental Kinematics"
    @staticmethod
    def getallweighted(set):
        return [
            ProblemSet.weigh(ETS17P1, 1)
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
            answer_ratio = force_ratio/accel_ratio
            identa = "m_A"
            identb = "m_B"

        answer_ratios, tcn = mh.similar_fractions_centered(answer_ratio, nanswers, seeda=ratio_A, seedb=ratio_B)
        sorted_answer_ratios, correctn = mh.sort_rational_answers(answer_ratios, tcn)

        statement = r"A net force $F_A$ acts on object $A$ and a net force $F_B$ acts on object $B$. "
        if mass_ratio != None:
            if (swap_mass):
                statement += "The mass of object $A$ is " + lh.linguistic_ratio(1/mass_ratio) + " the mass of object $B$. "
            else:
                statement += "The mass of object $B$ is " + lh.linguistic_ratio(mass_ratio) + " the mass of object $A$. "
        if force_ratio != None:
            if(swap_force):
                statement += "$F_A$ is " + lh.linguistic_ratio(1/force_ratio) + " $F_B$. "
            else:
                statement += "$F_B$ is " + lh.linguistic_ratio(force_ratio) + " $F_A$. "
        if accel_ratio != None:
            if (swap_accel):
                statement += "The acceleration of object $A$ is " + lh.linguistic_ratio(1/accel_ratio) + " that of object $B$. "
            else:
                statement += "The acceleration of object $B$ is " + lh.linguistic_ratio(accel_ratio) + " that of object $A$. "
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
                answers.append(NoEscape(r"$\displaystyle " + identb + " = " + lh.latex_fraction(ratio, oneblank=True) + identa + "$"))
            else:
                answers.append(NoEscape(r"$\displaystyle " + identa + " = " + lh.latex_fraction(1/ratio, oneblank=True) + identb + "$"))

        return {
            'statement':NoEscape(statement),
            'answers':answers,
            'correctn':correctn,
            'jumble':False
        }
