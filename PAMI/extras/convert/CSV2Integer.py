# csvToInteger is a code used to convert the csv into  Integer.
#
#  **Importing this algorithm into a python program**
#  --------------------------------------------------------
#
#             from PAMI.extras.csvParquet import csvToInteger as cp
#
#             obj = cp.csvToInteger(iFile, "\t ")
#
#             obj.save()
#
#             obj.csvToBitInteger("FileName") # To generate file in form  BitInteger.
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

import numpy as np
import pandas as pd

class csvToInteger:
    """
    :Description:   csvToInteger is a code used to convert the csv into  Integer

    :param  iFile: str :
            Name of the Input file
    :param  sep: str :
            This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.csvParquet import csvToInteger as cp

            obj = cp.csvToInteger(File, "\t")

            obj.save()

            obj.csvToBitInteger("FileName") # To generate file in form of BitInteger.

    """

    def __init__(self, iFile: str, sep: str = '\t'):
        self._iFile = iFile
        self._sep = sep


def csvToBitInteger(file, output, sep = "\t"):

    fileData = {}
    rename = {}
    counter = 0
    maxTS = 0


    with open(file,'r') as f:
        
        for line in f:
            line = line.strip().split(sep)
            timestamp = int(line[0])
            if timestamp > maxTS:
                maxTS = timestamp

            line = line[1:]

            for item in line:
                if item not in rename:
                    rename[item] = counter
                    counter += 1
                if rename[item] not in fileData:
                    fileData[rename[item]] = [timestamp]
                else:
                    fileData[rename[item]].append(timestamp)

    fileData = dict(sorted(fileData.items(), key = lambda x: len(x[1])))


    newRep = {}
    arraySize = maxTS // 32 + 1

    for k,v in fileData.items():
        bitRep = np.zeros(arraySize, dtype=np.uint32)
        for i in range(len(v)):
            bitRep[v[i] // 32] |= 1 << 31 - (v[i] % 32)
        newRep[k] = bitRep

    df = pd.DataFrame(newRep)
    df = df.T

    cols = []

    for i in range(len(df.columns)):
        cols.append(str(i))

    df.columns = cols

    df.to_parquet(output)



