from . import fundamentalkinematics
from ...base import ProblemGeneratorGroup
from ...base import ProblemSet

class AllProblems(ProblemGeneratorGroup):
    @staticmethod
    def getallweighted(set):
        return [
            ProblemSet.weigh(fundamentalkinematics.Group, 1)
        ]