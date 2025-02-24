# plotPointOnMap_dump is used to take the input patterns and plot the points on map.
#
#     **Importing this algorithm into a python program**
#     --------------------------------------------------------
#
#     from PAMI.extras.syntheticDataGenerator import plotPointOnMap_dump as plt
#
#     obj = plt.plotPointOnMap_dump(" ", 10, "\t")
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

import folium
import pandas as pd
from typing import Dict, List
import re

class plotPointOnMap:
    """
    :Description: plotPointOnMap is used to take the input patterns and plot the points on map

    :param  inputPatterns: str :   Name of the Input file
    :param  k: str :   Name of the FuzFile to process set of data.
    :param  sep: str :   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

                from PAMI.extras.syntheticDataGenerator import plotPointOnMap as plt

                obj = plt.plotPointOnMap(" ", 10, "\t")

                obj.save()

    """
    def __init__(self, inputPatterns: str, k: int=10, sep: str='\t'):
        self.inputPatterns = inputPatterns
        self.k = k
        self.sep = sep

    def findTopKPatterns(self) -> List[List[str]]: 
        Database = []
        if isinstance(self.inputPatterns, pd.DataFrame):
            patterns = []
            i = self.inputPatterns.columns.values.tolist()
            if 'Transactions' in i:
                patterns = self.inputPatterns['Patterns'].tolist()
            for pattern in patterns:
                if isinstance(pattern, str):
                    pattern = [item for item in pattern.strip().split(self.sep)]
                Database.append(pattern)
        elif isinstance(self.inputPatterns, dict):
            for pattern in self.inputPatterns:
                if isinstance(pattern, str):
                    pattern = [item for item in pattern.strip().split(self.sep)]
                Database.append(pattern)

        elif isinstance(self.inputPatterns, str):
            with open(self.inputPatterns, 'r') as f:
                for line in f:
                    pattern = [s for s in line.strip().split(':')][0]
                    pattern = [item for item in pattern.strip().split(self.sep)]
                    Database.append(pattern)

        patterns = sorted(Database, key=lambda x: len(x[0]), reverse=True)
        # return {patternId: patterns[patternId - 1] for patternId in range(1, int(self.k) + 1)}
        return patterns[:self.k]

    def convertPOINT(self, patterns: List[List[str]]) -> pd.DataFrame:
        locations = pd.DataFrame(columns=['patternId', 'latitude', 'longitude'])
        patternId = 1
        for pattern in patterns:
            for item in pattern:
                location = item.split(' ')
                longitude = re.sub('[^0-9. ]', '', location[0])
                latitude = re.sub('[^0-9. ]', '', location[1])
                df = pd.DataFrame([patternId, latitude, longitude], index=locations.columns).T
                locations = locations.append(df, ignore_index=True)
            patternId += 1
        return locations



    def plotPointInMap(self) -> folium.Map:
        topKPatterns = self.findTopKPatterns()
        df = self.convertPOINT(topKPatterns)
        mmap = folium.Map(location=[35.39, 139.44], zoom_start=5)
        # df = pd.read_csv(inputFile)
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen',
                  'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
        for i, row in df.iterrows():
            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                popup=row['patternId'],
                radius=3,
                # icon=folium.Icon(color=colors[int(row['patternId'])-1])
                color=colors[int(row['patternId']) - 1],
                fill=True,
                fill_color=colors[int(row['patternId']) - 1],
            ).add_to(mmap)
        return mmap

if __name__ == '__main__':
    obj = plotPointOnMap('/Users/nakamura0803/medicalDataAnalytics/test/disease/pattern_8842163_0.8.txt')
    mmap_ = obj.plotPointInMap()
    mmap_.save('map.html')
