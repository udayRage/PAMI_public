# SparseFormatDF in this code the dense dataframe is converting databases into different transactional, temporal, utility types.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.convert import sparseDF2DB as db
#
#             obj = db.sparseDF2DB(idf)
#
#             obj.save(oFile)
#
#             obj.convert2TransactionalDatabase("outputFileName", ">=", 16) # To create transactional database
#
#             obj.convert2TemporalDatabase("outputFileName", ">=", 16) # To create temporal database
#
#             obj.convert2UtilityDatabase("outputFileName") # To create utility database
#
#             obj.getFileName() # To get file name of the database
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
from typing import Union
class sparseDF2DB:
    """
    :Description:  This class create Data Base from DataFrame.

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

            from PAMI.extras.DF2DB import SparseFormatDF as db

            obj = db.SparseFormatDF(iDdf)

            obj.convert2TransactionalDatabase("outputFileName", ">=", 16) # To create transactional database

            obj.convert2TemporalDatabase("outputFileName", ">=", 16) # To create temporal database

            obj.convert2UtilityDatabase("outputFileName", ">=", 16) # To create utility database

            obj.getFileName("outputFileName", ">=", 16) # To get file name of the database
    """


    def __init__(self, inputDF) -> None:
        self.inputDF = inputDF
        self.condition = ""
        self.thresholdValue = 0
        self.outputFile = ''
        self.df = None
        
    def setParametors(self,outputFile: str, condition: str, thresholdValue:  Union[int, float]):
        self.condition = condition
        self.thresholdValue = thresholdValue
        self.outputFile = outputFile
        if self.condition == '>':
            self.df = self.inputDF.query(f'value > {self.thresholdValue}')
        elif self.condition == '>=':
            self.df = self.inputDF.query(f'value >= {self.thresholdValue}')
        elif self.condition == '<=':
            self.df = self.inputDF.query(f'value <= {self.thresholdValue}')
        elif self.condition == '<':
            self.df = self.inputDF.query(f'value < {self.thresholdValue}')
        else:
            print('Condition error')
        self.df = self.df.drop(columns='value')
        self.df = self.df.groupby('tid')['item'].apply(list)

    def convert2TransactionalDatabase(self, outputFile: str, condition: str, thresholdValue:  Union[int, float]) -> None:
        """
        Create transactional data base
        :param outputFile: str:
            Write transactional data base into outputFile
        :param condition: str :
            It is condition to judge the value in dataframe
        :param thresholdValue: int or float :
            User defined value.
        :return: None
        """
        self.setParametors(outputFile, condition, thresholdValue)
        with open(self.outputFile, 'w') as f:
            for line in self.df:
                f.write(f'{line[0]}')
                for item in line[1:]:
                    f.write(f',{item}')
                f.write('\n')

    def convert2TemporalDatabase(self, outputFile: str, condition: str, thresholdValue: float) -> None:
        """
        Create temporal data base
        :param outputFile: str:
            Write transactional data base into outputFile
        :param condition: str :
            It is condition to judge the value in dataframe
        :param thresholdValue: int or float :
            User defined value.
        :return: None
        """
        self.setParametors(outputFile, condition, thresholdValue)

        with open(self.outputFile, 'w') as f:
            for tid in self.df.index:
                f.write(f'{tid}')
                for item in self.df[tid]:
                    f.write(f',{item}')
                f.write('\n')

    def convert2UtilityDatabase(self, outputFile: str) -> None:
        """
        Create the utility database.
        :param outputFile: str:
            Write transactional database into outputFile
        :return: None
        """
        
        self.outputFile = outputFile
        items = self.inputDF.groupby(level=0)['item'].apply(list)
        values = self.inputDF.groupby(level=0)['value'].apply(list)
        sums = self.inputDF.groupby(level=0)['value'].sum()
        index = list(items.index)
        with open(self.outputFile, 'w') as f:
            for tid in index:
                f.write(f'{items[tid][0]}')
                for item in items[tid][1:]:
                    f.write(f'\t{item}')
                f.write(f':{sums[tid]}:')
                f.write(f'{values[tid][0]}')
                for value in values[tid][1:]:
                    f.write(f'\t{value}')
                f.write('\n')

    def getFileName(self) -> str:

        return self.outputFile

if __name__ == '__main__':

    obj = sparseDF2DB(sys.argv[1])
    obj.createTemporal(sys.argv[2],sys.argv[3],sys.argv[4])
    obj.getFileName()

