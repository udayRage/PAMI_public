# DF2DB in this code dataframe is converting databases into sparse or dense transactional, temporal, Utility.
#
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.DF2DB import DF2DB as db
#
#             obj = db.DF2DB(idf, "sparse/dense")
#
#             obj.convert2Transactional("outputFileName", ">=", 16) # To create transactional database
#
#             obj.convert2Temporal("outputFileName", ">=", 16) # To create temporal database
#
#             obj.convert2Utility("outputFileName") # To create utility database
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
import PAMI.extras.convert.denseDF2DB as dense
import PAMI.extras.convert.sparseDF2DB as sparse
import sys,psutil,os,time
from typing import Union
import operator

condition_operator = {
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne
}

class DF2DB:
    """
    :Description:  This class will create database for given DataFrame based on Threshold values and conditions are defined in the class.
                   Converts Dataframe into sparse or dense dataframes.

    :Attributes:

        :param inputDF: DataFrame :
             It is sparse or dense DataFrame
        :param thresholdValue: int or float :
             It is threshold value of all item
        :param condition: str :
             It is condition of all item
        :param DFtype: str :
             It is DataFrame type. It should be sparse or dense. Default DF is sparse.
        :param memoryUSS : float
            To store the total amount of USS memory consumed by the program
        :param memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        :param startTime : float
            To record the start time of the mining process
        endTime : float
            To record the completion time of the mining process


    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.DF2DB import DF2DB as db

            obj = db.DF2DB(idf, "sparse/dense")

            obj.convert2Transactional("outputFileName",condition,threshold) # To create transactional database

            obj.convert2Temporal("outputFileName",condition,threshold) # To create temporal database

            obj.convert2Utility("outputFileName",condition,threshold) # To create utility database
    """


    def __init__(self, inputDF, DFtype='dense') -> None:
        self.inputDF = inputDF
        self.DFtype = DFtype.lower()
        if DFtype == 'sparse':
            self.DF2DB = sparse.sparseDF2DB(self.inputDF)
        elif DFtype == 'dense':
            self.DF2DB = dense.denseDF2DB(self.inputDF)
        else:
            raise Exception('DF type should be sparse or dense')
        self._startTime = float()
        self._endTime = float()
        self._memoryUSS = float()
        self._memoryRSS = float()
        self.tids = []
        self.items = []
        self.items = list(self.inputDF.columns.values)
        self.tids = list(self.inputDF.index)

    def convert2TransactionalDatabase(self, oFile: str, condition: str, thresholdValue: Union[int, float]) -> None:
        """
        create transactional database and return oFileName
        :param oFile: file name or path to store database
        :type oFile: str
        :param condition: It is condition to judge the value
        :type condition: str
        :param thresholdValue: user defined threshold value
        :type thresholdValue: int or float
        """
        self._startTime = time.time()
        with open(oFile, 'w') as f:
            if condition not in condition_operator:
                print('Condition error')
            else:
                for tid in self.tids:
                    transaction = [item for item in self.items if
                                   condition_operator[condition](self.inputDF.at[tid, item], thresholdValue)]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f'\t{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction[0]}')
                    else:
                        continue
                    f.write('\n')
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        self._endTime  = time.time()

    def convert2TemporalDatabase(self, oFile: str, condition: str, thresholdValue: Union[int, float]) -> None:
        """
        create temporal database and return oFile name
        :param oFile: file name or path to store database
        :type oFile: str
        :param condition: It is condition to judge the value
        :type condition: str
        :param thresholdValue: user defined threshold value
        :type thresholdValue: int or float
        """
        self._startTime = time.time()
        with open(oFile, 'w') as f:
            if condition not in condition_operator:
                print('Condition error')
            else:
                for tid in self.tids:
                    transaction = [item for item in self.items if
                                   condition_operator[condition](self.inputDF.at[tid, item], thresholdValue)]
                    if len(transaction) > 1:
                        f.write(f'{tid + 1}')
                        for item in transaction:
                            f.write(f'\t{item}')
                    elif len(transaction) == 1:
                        f.write(f'{tid + 1}')
                        f.write(f'\t{transaction[0]}')
                    else:
                        continue
                    f.write('\n')
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        self._endTime  = time.time()

    def convert2UtilityDatabase(self, oFile: str) ->None:
        """
        create utility database and return oFile name
        :param oFile:  file name or path to store database
        :type oFile: str
        """
        self._startTime = time.time()
        with open(oFile, 'w') as f:
            for tid in self.tids:
                df = self.inputDF.loc[tid].dropna()
                f.write(f'{df.index[0]}')
                for item in df.index[1:]:
                    f.write(f'\t{item}')
                f.write(f':{df.sum()}:')
                f.write(f'{df.at[df.index[0]]}')

                for item in df.index[1:]:
                    f.write(f'\t{df.at[item]}')
                f.write('\n')
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        self._endTime = time.time()

    def convert2geoReferencedTransactionalDatabase(self, oFile: str, condition: str, thresholdValue: Union[int, float]) -> str:
        """
        create transactional database and return oFileName
        :param oFile: file name or path to store database
        :type oFile: str
        :param condition: It is condition to judge the value
        :type condition: str
        :param thresholdValue: user defined threshold value
        :type thresholdValue: int or float
        :rtype: str
        """
        self._startTime = time.time()
        with open(oFile, 'w') as f:
            if condition not in condition_operator:
                print('Condition error')
            else:
                for tid in self.tids:
                    transaction = [item for item in self.items if
                                   condition_operator[condition](self.inputDF.at[tid, item], thresholdValue)]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f'\t{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction[0]}')
                    else:
                        continue
                    f.write('\n')
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        self._endTime  = time.time()
        return self.DF2DB.getFileName()

    def convert2geoReferencedTemporalDatabase(self, oFile: str, condition: str, thresholdValue: Union[int, float]) -> str:
        """
        create temporal database and return oFile name
        :param oFile: file name or path to store database
        :type oFile: str
        :param condition: It is condition to judge the value
        :type condition: str
        :param thresholdValue: user defined threshold value
        :type thresholdValue: int or float
        :rtype: str
        """
        self._startTime = time.time()
        with open(oFile, 'w') as f:
            if condition not in condition_operator:
                print('Condition error')
            else:
                for tid in self.tids:
                    transaction = [item for item in self.items if
                                   condition_operator[condition](self.inputDF.at[tid, item], thresholdValue)]
                    if len(transaction) > 1:
                        f.write(f'{tid + 1}')
                        for item in transaction:
                            f.write(f'\t{item}')
                    elif len(transaction) == 1:
                        f.write(f'{tid + 1}')
                        f.write(f'\t{transaction[0]}')
                    else:
                        continue
                    f.write('\n')
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        self._endTime  = time.time()
        return self.DF2DB.getFileName()


    def convert2MultipleTimeSeries(self, oFile: str, condition: str,
                                   thresholdValue: Union[int, float], interval: int) -> None:
        """
        :Description: Create the multiple time series database.

        :param oFile:  Write multiple time series database into outputFile.
        :type oFile:  str
        :param interval: Breaks the given timeseries into intervals.
        :type interval: int
        :param condition: It is condition to judge the value in dataframe
        :param thresholdValue: User defined value.
        :type thresholdValue: int or float
        """
        self._startTime = time.time()
        writer = open(oFile, 'w+')
        # with open(self.outputFile, 'w+') as f:
        count = 0
        tids = []
        items = []
        values = []
        for tid in self.tids:
            count += 1
            transaction = [item for item in self.items if
                           condition_operator[condition](self.inputDF.at[tid, item], thresholdValue)]
            for i in transaction:
                tids.append(count)
                items.append(i)
                values.append(self.inputDF.at[tid, i])
            if count == interval:
                s1, s, ss = str(), str(), str()
                if len(values) > 0:

                    for j in range(len(tids)):
                        s1 = s1 + str(tids[j]) + '\t'
                    for j in range(len(items)):
                        s = s + items[j] + '\t'
                    for j in range(len(values)):
                        ss = ss + str(values[j]) + '\t'

                s2 = s1 + ':' + s + ':' + ss
                writer.write("%s\n" % s2)
                tids, items, values = [], [], []
                count = 0
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        self._endTime = time.time()



    def convert2UncertainTransactionalDatabase(self, oFile: str, condition: str,
                                       thresholdValue: Union[int, float]) -> None:
        with open(oFile, 'w') as f:
            if condition not in condition_operator:
                print('Condition error')
            else:
                for tid in self.tids:
                    transaction = [item for item in self.items if
                                   condition_operator[condition](self.inputDF.at[tid, item], thresholdValue)]
                    uncertain = [self.inputDF.at[tid, item] for item in self.items if
                                 condition_operator[condition](self.inputDF.at[tid, item], thresholdValue)]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f'\t{item}')
                        f.write(f':')
                        for value in uncertain:
                            tt = 0.1 + 0.036 * abs(25 - value)
                            tt = round(tt, 2)
                            f.write(f'\t{tt}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction[0]}')
                        tt = 0.1 + 0.036 * abs(25 - uncertain[0])
                        tt = round(tt, 2)
                        f.write(f':{tt}')
                    else:
                        continue
                    f.write('\n')


    def getMemoryUSS(self) -> float:
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self) -> float:
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self) -> float:
        """
        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime



if __name__ == '__main__':
    obj = DF2DB(sys.argv[1])
    obj.getTransactionalDatabase(sys.argv[2],sys.argv[3],sys.argv[4])
    print("Conversion is complete.")
    print("Total Memory in USS:", obj.getMemoryUSS())
    print("Total Memory in RSS", obj.getMemoryRSS())
    print("Total ExecutionTime in ms:", obj.getRuntime())
