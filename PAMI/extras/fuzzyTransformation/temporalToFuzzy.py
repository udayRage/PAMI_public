# temporalToFuzzy is used to convert the transactional database into Fuzzy transactional database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.FuzzyTransformation import temporalToFuzzy as db
#
#             obj = db.temporalToFuzzy(iFile, FuzFile, oFile, "\t" )
#
#             obj.startConvert()
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

from PAMI.extras.fuzzyTransformation import abstract as _ab


class temporalToFuzzy(_ab._convert):
    """

    :Description:
            temporalToFuzzy is used to convert the temporal database into Fuzzy temporal database.


    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  fuzFile: str :
                   Name of the Fuzzy File to process set of data.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.FuzzyTransformation import temporalToFuzzy as db

            obj = db.temporalToFuzzy(iFile, FuzFile, oFile, "\t" )

            obj.startConvert()

    """

    _iFile: str = ' '
    _fuzFile: str = ' '
    _oFile: str = ' '


    def __init__(self, iFile: str, fuzFile: str, oFile: str, sep: str = '\t'):
        super().__init__(iFile, fuzFile, oFile, sep)
        self._iFile = iFile
        self._fuzFile = fuzFile
        self._oFile = oFile
        self._sep = sep
        self._RegionsCal = []
        self._RegionsLabel = []
        self._LabelKey = {}
        self._LabelKeyOne = {}
        self._dbLen = 0
        self._list = []
        self._transactionsDB = []
        self._fuzzyValuesDB = []
        self._tsDB = []
        #self._fuzzyRegionReferenceMap = {}

    def _creatingItemSets(self) -> None:
        """
          To process the input file and store the timestamps, items, and their values as lists respectively.
        """
        self._transactionsDB, self._fuzzyValuesDB, self._tsDB = [], [], []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._transactionsDB = self._iFile['Transactions'].tolist()
            if 'fuzzyValues' in i:
                self._fuzzyValuesDB = self._iFile['Utilities'].tolist()

        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.decode("utf-8")
                    line = line.split("\n")[0]
                    parts = line.split(":")
                    items = parts[0].split(self._sep)
                    quantities = parts[1].split(self._sep)
                    self._tsDB.append(int(items[0]))
                    self._transactionsDB.append([x for x in items[1:]])
                    self._fuzzyValuesDB.append([x for x in quantities])
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            parts = line.split(":")
                            parts[0] = parts[0].strip()
                            parts[1] = parts[1].strip()
                            items = parts[0].split(self._sep)
                            quantities = parts[1].split(self._sep)
                            self._tsDB.append(int(items[0]))
                            self._transactionsDB.append([x for x in items[1:]])
                            self._fuzzyValuesDB.append([x for x in quantities])
                except IOError:
                    print("File Not Found")
                    quit()

    def _fuzzyMembershipFunc(self) -> None:
        """
        The Fuzzy file is processed and labels created according the boundaries specified in input file.
        """
        try:
            with open(self._fuzFile, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    line = line.split("\n")[0]
                    parts = line.split(self._sep)
                    lowerBound = parts[0].strip()
                    upperBound = parts[1].strip()
                    lb_Label = parts[2].strip()
                    ub_Label = parts[3].strip()
                    self._RegionsCal.append([int(lowerBound), int(upperBound)])
                    self._RegionsLabel.append([lb_Label, ub_Label])
                    for i in range(0, 2):
                        if ub_Label not in self._LabelKey:
                            self._LabelKey[ub_Label] = count
                            count += 1
            self._LabelKeyOne = {v: k for k, v in self._LabelKey.items()}
        except IOError:
            print("File Not Found")
            quit()

    def _Regions(self, quantity: int) -> None:
        """
        calculate the labelled region of input "quantity"
        :param quantity: represents the quantity of item
        :type quantity: int
        :return: None
        """
        self._list = [0] * len(self._LabelKey)
        if self._RegionsCal[0][0] < quantity <= self._RegionsCal[0][1]:
            self._list[0] = 1
            return
        elif quantity >= self._RegionsCal[-1][0]:
            self._list[-1] = 1
            return
        else:
            for i in range(1, len(self._RegionsCal) - 1):
                if self._RegionsCal[i][0] <= quantity <= self._RegionsCal[i][1]:
                    base = self._RegionsCal[i][1] - self._RegionsCal[i][0]
                    self._list[self._LabelKey[self._RegionsLabel[i][0]]] = float((self._RegionsCal[i][1] - quantity) / base)
                    self._list[self._LabelKey[self._RegionsLabel[i][1]]] = float((quantity - self._RegionsCal[i][0]) / base)
            return

    def startConvert(self) -> None:
        """
        Main method to convert the temporal database into fuzzy database.
        """
        _writer = open(self._oFile, 'w+')
        self._creatingItemSets()
        self._fuzzyMembershipFunc()
        for line in range(len(self._transactionsDB)):
            item_list = self._transactionsDB[line]
            fuzzyValues_list = self._fuzzyValuesDB[line]
            self._dbLen += 1
            s = str(self._tsDB[line])
            ss = str()
            for i in range(0, len(item_list)):
                item = item_list[i]
                fuzzy_ref = fuzzyValues_list[i]
                self._Regions(int(fuzzy_ref))
                #self._fuzzyRegionReferenceMap[fuzzy_ref] = regionsList
                s1 = [self._list.index(i) for i in self._list if i!=0]
                for k in s1:
                    s = s + item + '.' + self._LabelKeyOne[k] + '\t'
                    st = round(self._list[k], 2)
                    ss = ss + str(st) + '\t'
            s2 = s.strip('\t') + ":" + ss
            _writer.write("%s \n" % s2)



if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = temporalToFuzzy(_ab._sys.argv[1], _ab._sys.argv[2], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = temporalToFuzzy(_ab._sys.argv[1], _ab._sys.argv[2],  _ab._sys.argv[3])
        _ap.startConvert()
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
