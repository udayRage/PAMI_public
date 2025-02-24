import pandas as pd
import numpy as np
import sys
# DB2DF in this code transactional databases is converting dense dataframe.
#**Importing this algorithm in terminal**
#             python3 DB2DF inputFileName outputFileName separator
# 
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.DB2DF import DB2DF as db
#
#             obj = db.DB2DF(fileName)
#
#             obj.createDB()
#            
#             df=obj.getDF()
#
#             obj.save(outputFileName)
#
"""
Copyright (C)  2024 Rage Uday Kiran

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
"""     
class TransactionDB2denseDF:
    """
    :Description:  DB2DF in this code transactional databases is converting dense dataframe.

    :Attributes:

        :param _iFile: str :
             It is input file name.
        :param _sep: str :
             It is separator for each values. Default is '\t'.
        :param _oFile: str :
             It is output file name. Default is 'TransactialDB'+inputFile+".csv".
        :param _Database: str :
             It is database made from file.
        :param df: DataFrame :
             It is dense DataFrame.


    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

             from PAMI.extras.DB2DF import DF2DF as db
            
             obj = db.DF2DF(fileName)

             obj.createDB()
            
             df=obj.getDF()#get the dataframe

             obj.save(outputFileName)#get the dataframe by csv
    """

    def __init__(self, inputFile,sep=" ") -> None:
        self._iFile = inputFile
        self._sep=sep
        self._Database=[]
        self.oFile = 'TransactialDB'+inputFile+".csv"
        self._df = pd.DataFrame()
    def _get_unique_list(self):
        """
        create transactional database and return outputFileName
        :type seen: list
        :return: seen
        """
        seen = []
        for items in self._Database:
            for item in items:
                if item not in seen:
                    seen.append(item)
                
        return seen
        
    
    def _creatingItemSets(self) -> None:
            """
            Storing the complete transactions of the database/input file in a database variable
            """
            self._Database = []
            if isinstance(self._iFile, pd.DataFrame):
                temp = []
                if self._iFile.empty:
                    print("its empty..")
                i = self._iFile.columns.values.tolist()
                if 'Transactions' in i:
                    self._Database = self._iFile['Transactions'].tolist()
                    self._Database = [x.split(self._sep) for x in self._Database]
                else:
                    print("The column name should be Transactions and each line should be separated by tab space or a seperator specified by the user")
            if isinstance(self._iFile, str):
                
                    try:
                        with open(self._iFile, 'r', encoding='utf-8') as f:
                            for line in f:
                                line.strip()
                                temp = [i.rstrip() for i in line.split(self._sep)]
                                temp = [x for x in temp if x]
                                self._Database.append(set(temp))
                    except IOError:
                        print("File Not Found")
                        quit()

    def makeDic(self):
        """
        create dence dataframe 
        """
        column=self._get_unique_list()
        self._df = pd.DataFrame(index=range(len(self._Database)),columns=column)
        
        self._df.fillna(0, inplace=True)
        index=0
        for items in self._Database:
            for item in items:
                self._df.loc[index,str(item)]=1
            index+=1
                
    def save(self,oFile):
        """
        save database in csv file
        :input 
            oFile:str    output file name
        """
        self._df.to_csv(oFile,index=False)
    def createDB(self):
        
        self._creatingItemSets()
        self.makeDic()
    def getDF(self):
        """
        get database 
        :return: df
        """
        return self._df
        
if __name__ == '__main__':

    if len(sys.argv)==3:
        obj = TransactionDB2denseDF( sys.argv[0], sys.argv[2])
        obj.createDB()
        obj.save(sys.argv[1])
    elif len(sys.argv)==2:
        obj = TransactionDB2denseDF( sys.argv[0])
        obj.createDB()
        obj.save(sys.argv[1])
    elif len(sys.argv)==1:
        obj = TransactionDB2denseDF( sys.argv[0])
        obj.createDB()
        #self.save(obj.oFile)
    else:
        print("Err:wrong input")