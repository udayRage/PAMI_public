from abc import ABC, abstractmethod
from .graph import UncertainGraph
from .vertex import Vertex
from .edge import Edge
from .dfsCode import DFSCode

import math
import random
from copy import deepcopy

import itertools


class _MUSE(ABC):

        @abstractmethod
        def mine(self, minsup, epsilon, delta):
            """
            Run the muse algorithm.
            """
            pass

        @abstractmethod
        def readGraph(self, path):
            """
            Read graphs from a file.
            :param path: Path to the file containing the graphs.
            """
            pass

        @abstractmethod
        def save(self, oFile):
            """
            Write the result of the muse algorithm to a file.
            :param oFile: Path to the output file.
            """
            pass

