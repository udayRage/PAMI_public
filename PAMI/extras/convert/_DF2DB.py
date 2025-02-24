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
import sys
from typing import Union

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
    def convert2TransactionalDatabase(self, oFile: str, condition: str, thresholdValue: Union[int, float]) -> str:
        """
        create transactional database and return oFileName
        :param oFile: file name or path to store database
        :type oFile: str
        :param condition: condition
        :type condition: str
        :param thresholdValue: threshold value
        :type thresholdValue: int or float
        :return: oFile name
        :rtype: str
        """
        self.DF2DB.convert2TransactionalDatabase(oFile,condition,thresholdValue)
        return self.DF2DB.getFileName()

    def convert2TemporalDatabase(self, oFile: str, condition: str, thresholdValue: Union[int, float]) -> str:
        """
        create temporal database and return oFile name
        :param oFile: file name or path to store database
        :type oFile: str
        :param condition: condition
        :type condition: str
        :param thresholdValue: threshold value
        :type thresholdValue: int or float
        :return: oFile name
        :rtype: str
        """
        self.DF2DB.convert2TemporalDatabase(oFile,condition,thresholdValue)
        return self.DF2DB.getFileName()

    def convert2UtilityDatabase(self, oFile: str) -> str:
        """
        create utility database and return oFile name
        :param oFile:  file name or path to store database
        :type oFile: str
        :return: outputFile name
        :rtype: str
        """
        self.DF2DB.convert2UtilityDatabase(oFile)
        return self.DF2DB.getFileName()


if __name__ == '__main__':
    obj = DF2DB(sys.argv[1])
    obj.getTransactionalDatabase(sys.argv[2],sys.argv[3],sys.argv[4])