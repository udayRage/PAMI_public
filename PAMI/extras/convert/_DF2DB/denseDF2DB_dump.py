# DenseFormatDF_dump in this code the dense dataframe is converting databases into different transactional, temporal, utility types.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.DF2DB import DenseFormatDF_dump as db
#
#             obj = db.DenseFormatDF_dump(idf, ">=", 16)
#
#             obj.save(oFile)
#
#             obj.createTransactional("outputFileName") # To create transactional database
#
#             obj.createTemporal("outputFileName") # To create temporal database
#
#             obj.createUtility("outputFileName") # To create utility database
#
#             obj.getFileName("outputFileName") # To get file name of the database
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

import pandas as pd
import sys
class DenseFormatDF:
    """
    :Description: This class create Data Base from DataFrame.

    :Attributes:

        :param inputDF: dataframe :
            It is dense DataFrame
        :param condition: str :
            It is condition to judge the value in dataframe
        :param thresholdValue: int or float :
            User defined value.

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.DF2DB import DenseFormatDF_dump as db

            obj = db.DenseFormatDF_dump(iDdf, ">=", 16)

            obj.save(oFile)

            obj.createTransactional("outputFileName") # To create transactional database

            obj.createTemporal("outputFileName") # To create temporal database

            obj.createUtility("outputFileName") # To create utility database

            obj.getFileName("outputFileName") # To get file name of the database

    """

    def __init__(self, inputDF, condition: str, thresholdValue: float) -> None:
        self.inputDF = inputDF
        self.condition = condition
        self.thresholdValue = thresholdValue
        self.tids = []
        self.items = []
        self.outputFile = ' '
        self.items = list(self.inputDF.columns.values)[1:]
        self.inputDF = self.inputDF.set_index('tid')
        self.tids = list(self.inputDF.index)


    def createTransactional(self, outputFile: str) -> None:
        """
        :Description: Create transactional data base

        :param outputFile: Write transactional data base into outputFile

        :type outputFile: str

        :return: None

        """

        self.outputFile = outputFile
        with open(outputFile, 'w') as f:
            if self.condition == '>':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] > self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction}')
                    else:
                        continue
                    f.write('\n')

            elif self.condition == '>=':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] >= self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction}')
                    else:
                        continue
                    f.write('\n')

            elif self.condition == '<=':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] <= self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction}')
                    else:
                        continue
                    f.write('\n')

            elif self.condition == '<':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] < self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction}')
                    else:
                        continue
                    f.write('\n')
            elif self.condition == '==':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] == self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction}')
                    else:
                        continue
                    f.write('\n')
            elif self.condition == '!=':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] != self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction}')
                    else:
                        continue
                    f.write('\n')
            else:
                print('Condition error')



    def createTemporal(self, outputFile: str) -> None:
        """
        :Description: Create temporal data base

        :param outputFile: Write temporal data base into outputFile

        :type outputFile: str

        :return: None
        """

        self.outputFile = outputFile
        with open(outputFile, 'w') as f:
            if self.condition == '>':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] > self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{tid}')
                        for item in transaction:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{tid}')
                        f.write(f',{transaction}')
                    else:
                        continue
                    f.write('\n')

            elif self.condition == '>=':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] >= self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{tid}')
                        for item in transaction:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{tid}')
                        f.write(f',{transaction}')
                    else:
                        continue
                    f.write('\n')

            elif self.condition == '<=':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] <= self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{tid}')
                        for item in transaction:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{tid}')
                        f.write(f',{transaction}')
                    else:
                        continue
                    f.write('\n')

            elif self.condition == '<':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] < self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{tid}')
                        for item in transaction:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{tid}')
                        f.write(f',{transaction}')
                    else:
                        continue
                    f.write('\n')
            elif self.condition == '==':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] == self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{tid}')
                        for item in transaction:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{tid}')
                        f.write(f',{transaction}')
                    else:
                        continue
                    f.write('\n')
            elif self.condition == '!=':
                for tid in self.tids:
                    transaction = [item for item in self.items if self.inputDF.at[tid, item] != self.thresholdValue]
                    if len(transaction) > 1:
                        f.write(f'{tid}')
                        for item in transaction:
                            f.write(f',{item}')
                    elif len(transaction) == 1:
                        f.write(f'{tid}')
                        f.write(f',{transaction}')
                    else:
                        continue
                    f.write('\n')

            else:
                print('Condition error')

    def createUtility(self, outputFile: str) -> None:
        """

        :Description: Create the utility database.

        :param outputFile:  Write utility database into outputFile

        :type outputFile: str

        :return: None

        """

        self.outputFile = outputFile
        with open(self.outputFile, 'w') as f:
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

    def getFileName(self) -> str:
        """
        :return: outputFile name

        :rtype: str
        """

        return self.outputFile


if __name__ == '__main__':


    obj = DenseFormatDF(sys.argv[1], sys.argv[2],float(sys.argv[3]))
    obj.getFileName()

