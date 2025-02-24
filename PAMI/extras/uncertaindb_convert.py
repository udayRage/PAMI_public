# uncertaindb_convert is used to convert the given database and predict classes.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#     from PAMI.extras.syntheticDataGenerator import uncertaindb_convert as un
#
#     obj = un.predictedClass2Transaction(predicted_classes, 0.8)
#
#     obj.save()
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


class predictedClass2Transaction:
    """
    :Description: This is used to convert the given database and predict classes.

    :param predicted_classes: list: It is dense DataFrame

    :param minThreshold: int or float : minimum threshold User defined value.


    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

                from PAMI.extras.syntheticDataGenerator import uncertaindb_convert as un

                obj = un.uncertaindb_convert(predicted_classes, 0.8)

                obj.save(oFile)

    """
    def __init__(self, predicted_classes: list,minThreshold: float =0.8) :
        self.predicted_classes = predicted_classes
        self.minThreshold = minThreshold
        self.predictions_dict = {}
    def getBinaryTransaction(self,predicted_classes: list,minThreshold: float =0.8) -> dict:

        for name, p, box in predicted_classes:
            if p > minThreshold :
                    if name not in self.predictions_dict:
                        self.predictions_dict[name] = [p, ]
                    else:
                        self.predictions_dict[name].append(p)
        return self.predictions_dict
