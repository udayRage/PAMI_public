# convertMultiTSIntoFuzzy is a code used to convert the multiple time series into fuzzy
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#     from PAMI.extras.syntheticDataGenerator import convertMultiTSIntoFuzzy as fuz
#
#     obj = fuz.convertMultiTSIntoFuzzy(iFile, FuzFile)
#
#     obj.save()
#
#     obj.mine()
#




__copyright__ = """
Copyright (C)  2021 Rage Uday Kiran

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import time
from statistics import stdev
import sys
import pandas as pd
import plotly.express as px

class convertMultipleTSIntoFuzzy:
    """
    :Description: Converting multiple time series into fuzzy

    :param  iFile: str :
                Name of the Input file
    :param  FuzFile: str :
                Name of the FuzFile to process set of data.

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

                from PAMI.extras.syntheticDataGenerator import convertMultiTSIntoFuzzy as fuz

                obj = fuz.convertMultiTSIntoFuzzy(iFile, FuzFile)

                obj.save()

                obj.mine()

    """


    def __init__(self, iFile: str,  FuzFile: str) -> None:
        #super().__init__(iFile, nFile, FuzFile, minSup, maxPer, sep)
        self._iFile = iFile
        self._FuzFile = FuzFile
        self._RegionsCal = []
        self._RegionsLabel = []
        self._LabelKey = {}
        self._LabelKeyOne = {}
        self._fuzzyRegionReferenceMap = {}
        self._finalPatterns = {}

    def _fuzzyMembershipFunc(self) -> None:
    
        try:
            with open(self._FuzFile, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    line = line.strip()
                    line = line.split("\n")[0]
                    parts = line.split(" ")
                    lowerBound = parts[0].strip()
                    upperBound = parts[1].strip()
                    lb_Label = parts[2].strip()
                    ub_Label = parts[3].strip()
                    self._RegionsCal.append([int(lowerBound), int(upperBound)])
                    self._RegionsLabel.append([lb_Label, ub_Label])
                    for i in range(0, 2):
                        if lb_Label.capitalize() not in self._LabelKey:
                            self._LabelKey[lb_Label.capitalize()] = count
                            count += 1
                        if ub_Label.capitalize() not in self._LabelKey:
                            self._LabelKey[ub_Label.capitalize()] = count
                            count += 1
            self._LabelKeyOne = {v:k for k,v in self._LabelKey.items()}
        except IOError:
            print("File Not Found")
            quit()

    def _creatingItemSets(self) -> None:
        self._transactionsDB, self._fuzzyValuesDB, self._timeEvents = [], [], []
        try:
            with open(self._iFile, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    line = line.split("\n")[0]
                    parts = line.split(":")
                    parts[0] = parts[0].strip()
                    parts[1] = parts[1].strip()
                    parts[2] = parts[2].strip()
                    times = parts[0].split('\t')
                    items = parts[1].split('\t')
                    quantities = parts[2].split('\t')
                    self._timeEvents.append([x for x in times if x])
                    self._transactionsDB.append([x for x in items if x])
                    self._fuzzyValuesDB.append([x for x in quantities if x])
        except IOError:
            print("File Not Found")
            quit()

    def _Regions(self, quantity: float) -> None:

        self.list = [0] * len(self._LabelKey)
        if self._RegionsCal[0][0] < quantity <= self._RegionsCal[0][1]:
            self.list[0] = 1
            return
        elif quantity >= self._RegionsCal[-1][0]:
            self.list[-1] = 1
            return
        else:
            for i in range(1, len(self._RegionsCal) - 1):
                if self._RegionsCal[i][0] < quantity <= self._RegionsCal[i][1]:
                    base = self._RegionsCal[i][1] - self._RegionsCal[i][0]
                    for pos in range(0, 2):
                        if self._RegionsLabel[i][pos].islower():
                            self.list[self._LabelKey[self._RegionsLabel[i][pos].capitalize()]] = float(
                                (self._RegionsCal[i][1] - quantity) / base)
                        else:
                            self.list[self._LabelKey[self._RegionsLabel[i][pos].capitalize()]] = float(
                                (quantity - self._RegionsCal[i][0]) / base)
            return
       
    def save(self, outputFile: str) -> None:
        self.mine()
        writer = open(outputFile, 'w+')
        for line in range(len(self._transactionsDB)):
            item_list = self._transactionsDB[line]
            fuzzyValues_list = self._fuzzyValuesDB[line]
            times = self._timeEvents[line]
            s = str()
            s2 = str()
            s1, s, ss = str(), str(), str()
            for i in range(0, len(item_list)):
                item = item_list[i]
                fuzzy_ref = fuzzyValues_list[i]
                #if type(fuzzy_ref) == int:
                self._Regions(float(fuzzy_ref))
                # else:
                #     self._Regions(float(fuzzy_ref))
                self._fuzzyRegionReferenceMap[fuzzy_ref] = self.list
                values = [self.list.index(i) for i in self.list if i!=0]
                for k in values:
                    s1 = s1 + times[i] + '\t'
                    s = s +  item + '.' + self._LabelKeyOne[k]  + '\t'
                    ss = ss + str(round(self.list[k], 2))+ '\t'
            s2 = s1 + ':' + s + ':' + ss
            # print(s2)
            # break
            writer.write("%s\n" %s2)

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Frequent pattern mining process will start from here
        """
        
        self._creatingItemSets()
        self._fuzzyMembershipFunc()


    def mine(self) -> None:
        """
        Frequent pattern mining process will start from here
        """

        self._creatingItemSets()
        self._fuzzyMembershipFunc()
        self._finalPatterns = {}
        
if __name__ == "__main__":
    convertMultipleTSIntoFuzzy(sys.argv[1], sys.argv[2])









