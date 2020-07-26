import random

import numpy as np
from abc import ABC, abstractmethod

from pylatex import *
from pylatex.base_classes import Container, Environment
from pylatex.utils import italic, NoEscape


def generatetest(*, nquestions=100, nanswers=5, generatorset=None):
    arrangement = generatorset.arrange(nquestions)

    problemset = []
    answerkey = []

    pnum = 0
    for weightedgenerator in arrangement:
        pnum += 1
        generator = weightedgenerator["generator"]
        statement, answers, correct, shuffle = generator.generate(nanswers)
        finalanswers = answers
        finalcorrect = correct
        if shuffle:
            shuffledanswers = list(enumerate(answers))
            random.shuffle(shuffledanswers)
            finalanswers = [answer for (i, answer) in shuffledanswers]
            scorrect = 0
            for (i, answer) in shuffledanswers:
                if (i == correct):
                    break
                scorrect += 1
            finalcorrect = scorrect

        problemset.append(makeproblem(pnum, statement, finalanswers))
        answerkey.append(makeanswer(finalcorrect))

    return maketestdoc(problemset, answerkey).dumps()


def makeproblem(pnum, statement, answers):
    probfrag = Fragment()
    with probfrag.create(SamePage()):
        probfrag.append(statement)
        probfrag.append('\n')
        with probfrag.create(Enumerate(enumeration_symbol=r"(\Alph*)")) as enum:
            for answer in answers:
                enum.add_item(answer)
    return probfrag


def makeanswer(correct):
    return colnum_string(correct + 1)


# Thank you, https://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter
def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def maketestdoc(problemset, answerkey):
    doc = Document(document_options='12pt',
                   geometry_options={"tmargin": "2cm", "lmargin": "1cm", "rmargin": "1cm", "bmargin": "2cm"})

    doctitle = 'Auto-Generated Physics GRE Practice Test'
    doc.preamble.append(Command('title', doctitle))
    doc.append(Command('maketitle'))

    pagestyle = PageStyle("header", header_thickness=1, footer_thickness=1)
    with pagestyle.create(Head("L")) as head:
        head.append(Command('slshape'))
        head.append(doctitle)

    with pagestyle.create(Foot("L")) as foot:
        foot.append(Command('slshape'))
        foot.append("https://github.com/GeorgesOatesLarsen/Physics-GRE-Testgen")

    with pagestyle.create(Foot("R")) as foot:
        foot.append(Command('slshape'))
        foot.append(Command('thepage'))

    doc.preamble.append(pagestyle)
    doc.change_document_style("header")
    doc.preamble.append(Command("twocolumn"))
    doc.preamble.append(Command('linespread', arguments=['1.25']))

    with doc.create(Section('Practice Test')):
        with doc.create(Enumerate()) as enum:
            for problem in problemset:
                enum.add_item(problem)

    doc.append(Command("clearpage"))

    with doc.create(Section('Answer Key')):
        with doc.create(Enumerate()) as enum:
            for answer in answerkey:
                enum.add_item(answer)

    return doc


class ProblemGenerator(ABC):
    @staticmethod
    @abstractmethod
    def generate(nanswers):
        pass

    @staticmethod
    @abstractmethod
    def getname():
        pass

    @staticmethod
    @abstractmethod
    def getcategory():
        pass


class ProblemSet:
    def __init__(self, group):
        self.generators = []
        self.weights = []
        self.totalweight = 0
        self.register(group, 1)

    def register(self, who, weight, category=None):
        if issubclass(who, ProblemGeneratorGroup):
            localweighttotal = 0
            for weightedgenerator in who.getallweighted(self):
                localweighttotal += weightedgenerator['weight']
            for weightedgenerator in who.getallweighted(self):
                self.register(weightedgenerator['generator'],
                              weightedgenerator['weight'] / localweighttotal * weight,
                              weightedgenerator['category'])
        elif issubclass(who, ProblemGenerator):
            self.generators.append({
                'generator': who,
                'weight': weight,
                'category': category
            })
            self.weights.append(weight)
            self.totalweight += weight

    def arrange(self, nproblems):
        return random.choices(self.generators, weights=self.weights, k=nproblems)

    @staticmethod
    def weigh(generator, weight, category=None):
        return {
            'generator': generator,
            'weight': weight,
            'category': category,
        }


class ProblemGeneratorGroup(ABC):
    @staticmethod
    @abstractmethod
    def getallweighted(set):
        pass


class Fragment(Container):
    """A LaTeX fragment container class for fragmented document construction."""

    def __init__(self, **kwargs):
        """
        Args
        ----
        """

        super().__init__(**kwargs)

    def dumps(self):
        """Represent the fragment as a string in LaTeX syntax.
        Returns
        -------
        str
        """

        return self.dumps_content()


class SamePage(Environment):
    _latex_name = 'samepage'
    packages = [Package("amsmath")]


class Equation(Environment):
    _latex_name = 'equation*'
