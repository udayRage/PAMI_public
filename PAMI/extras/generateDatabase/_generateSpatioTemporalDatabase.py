# generateSpatioTemporalDatabase is a code used to convert the database into SpatioTemporal database.
#
#   **Importing this algorithm into a python program**
#   --------------------------------------------------------
#
#             from PAMI.extras.generateDatabase import generateSpatioTemporalDatabase as db
#
#             obj = db.generateSpatioTemporalDatabase(0, 100, 0, 100, 10, 10, 0.5, 0.9, 0.5, 0.9)
#
#             obj.save()
#
#             obj.createPoint(0,100,0,100) # values can be according to the size of data
#
#             obj.saveAsFile("outputFileName") # To create a file
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
import random as rand
from typing import List, Dict, Tuple, Set, Union, Any, Generator
import pandas
import sys

class spatioTemporalDatabaseGenerator:
    """

    :Description:   generateSpatioTemporalDatabase is a code used to convert the database into SpatioTemporal database.

    :param  xmin: int :
            To give minimum value for x
    :param  xmax: int :
            To give maximum value for x
    :param  ymin: int :
            To give minimum value for y
    :param  ymax: int :
             To give maximum value for y
    :param maxTimeStamp: int :
            maximum Time Stamp for the database
    :param numberOfItems: int :
            number of items in the database
    :param itemChanceLow: int or float :
            least chance for item in the database
    :param itemChanceHigh: int or float :
            highest chance for item in the database
    :param timeStampChanceLow: int or float :
            lowest time stamp value
    :param timeStampChanceHigh: int or float:
            highest time stamp value

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.generateDatabase import generateSpatioTemporalDatabase as db

            obj = db.generateSpatioTemporalDatabase(0, 100, 0, 100, 10, 10, 0.5, 0.9, 0.5, 0.9)

            obj.save(oFile)

            obj.createPoint(0,100,0,100) # values can be according to the size of data

            obj.saveAsFile("outputFileName") # To create a file

    """

    coinFlip = [True, False]
    timestamp = list()
    items = list()
    alreadyAdded = set()
    outFileName=""

    def createPoint(self, xmin: int, xmax: int, ymin: int, ymax: int) -> Tuple[int, int]:
        x = rand.randint(xmin, xmax)
        y = rand.randint(ymin, ymax)
        coordinate = tuple([x, y])
        return coordinate

    def __init__(self,xmin: int,xmax: int,ymin: int,ymax: int,maxTimeStamp: int,numberOfItems: int, itemChanceLow: float,
                 itemChanceHigh: float, timeStampChanceLow: float,
                 timeStampChanceHigh: float) -> None:
        coinFlip = [True, False]
        timeStamp = 1
        self.timeStampList = list()
        self.itemList = list()

        while timeStamp != maxTimeStamp + 1:
            itemSet=list()
            for i in range(1, numberOfItems+1):
                #rand1=rand.rand(itemChanceLow,itemChanceHigh)
                #rand2 = rand.rand(timeStampChanceLow, timeStampChanceHigh)
                if rand.choices(coinFlip, weights=[itemChanceLow,itemChanceHigh], k=1)[0]:
                    coordinate=self.createPoint(xmin, xmax, ymin, ymax)
                    coordinate=tuple(coordinate)
                    if coordinate not in self.alreadyAdded:
                        coordinate=list(coordinate)
                        itemSet.append(coordinate)
                        coordinate=tuple(coordinate)
                        self.alreadyAdded.add(coordinate)
            if itemSet:
                self.timeStampList.append(
                    timeStamp)
                self.itemList.append(
                    itemSet)
            if rand.choices(coinFlip, weights=[itemChanceLow,itemChanceHigh], k=1)[0]:
                 timeStamp += 1
        self.outFileName = "temporal_" + str(maxTimeStamp // 1000) + \
                           "KI" + str(numberOfItems) + "C" + str(itemChanceLow) + "T" + str(timeStampChanceLow) + ".csv"




    def saveAsFile(self, outFileName="", sep="\t") -> None:
        if outFileName != "":
            self.outFileName = outFileName

        file = open(
            self.outFileName, "w")

        for i in range(len(self.timeStampList)):
            file.write(
                str(self.timeStampList[i]))
            for j in range(len(self.itemList[i])):
                file.write(
                    sep + str(self.itemList[i][j]))
            file.write('\n')

        file.close()


if __name__ == "__main__":
    xmin_=0
    xmax_=100
    ymin_=0
    ymax_=100
    maxTimeStamp_ = 10
    numberOfItems_ = 10
    itemChanceLow_ = 0.5
    itemChanceHigh_ = 0.9
    timeStampChanceLow_ = 0.5
    timeStampChanceHigh_ = 0.9
    obj = spatioTemporalDatabaseGenerator(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),float(sys.argv[7]),float(sys.argv[8]),float(sys.argv[9]),float(sys.argv[10]))
    obj.saveAsFile(sys.argv[11])
