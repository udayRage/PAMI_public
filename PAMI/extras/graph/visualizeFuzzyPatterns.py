# visualizeFuzzyPatterns is used to visualize points produced by pattern miner .
#
#  **Importing this algorithm into a python program**
#  --------------------------------------------------------
#
#     from PAMI.extras.graph import visualizeFuzzyPatterns as viz
#
#     obj = viz.visualizeFuzzyPatterns(iFile, topk)
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
# from PAMI.extras.graph import visualizePatterns as fig

# obj = fig.visualizePatterns('soramame_frequentPatterns.txt',50)
# obj.visualize(width=1000,height=900)

import plotly.express as px
import pandas as pd
import sys


class visualizeFuzzyPatterns:
    """

   :Description:   visualizeFuzzyPatterns is used to visualize points produced by pattern miner .
   :Attributes:

   :param file : file:   store input data as file
   :param topk : int:     Takes the value int as input

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.graph import visualizeFuzzyPatterns as viz

            obj = viz.visualizeFuzzyPatterns(iFile, topk)

            obj.save()
    """

    def __init__(self, file: str, topk: int) -> None:
        self.file = file
        self.topk = topk

    def visualize(self, markerSize: int = 20, zoom: int = 3, width: int = 1500, height: int = 1000) -> None:
        """
        Visualize points produced by pattern miner.

        :param markerSize: Size of the marker
        :type markerSize: int
        :param zoom: Zoom level
        :type zoom: int
        :param width: Width of the graph
        :type width: int
        :param height: Height of the graph on the screen
        :type width: int
        :return: None
        """

        long = []
        lat = []
        name = []
        color = []
        R = G = B = 0

        lines = {}
        with open(self.file, "r") as f:
            for line in f:
                lines[line] = len(line)

        lines = list(dict(sorted(lines.items(), key=lambda x: x[1])[-self.topk:]).keys())

        start = 1

        print("Number \t Pattern")
        for line in lines:

            start += 1
            if start % 3 == 0:
                R += 20
            if start % 3 == 1:
                G += 20
            if start % 3 == 2:
                B += 20
            if R > 255:
                R = 0
            if G > 255:
                G = 0
            if B > 255:
                B = 0
            RHex = hex(R)[2:]
            GHex = hex(G)[2:]
            BHex = hex(B)[2:]
            line = line.split(":")
            freq = line[-1]
            freq = "Frequency: " + freq.strip()
            line = line[:-1]
            print(str(start) + "\t" + line[0])
            points = line[0].split("\t")
            points = [x for x in points if x != ""]
            points = [x.strip("Point())") for x in points]
            for i in range(len(points)):
                rrr = points[i][8:29]
                temp = rrr.split()
                temp = [i.strip("()") for i in temp]
                lat.append(float(temp[0]))
                long.append(float(temp[1]))
                name.append(freq)
                color.append("#" + RHex + GHex + BHex)
        df = pd.DataFrame({"lon": long, "lat": lat, "freq": name, "col": color})

        fig = px.scatter_mapbox(df, lat="lon", lon="lat", hover_name="freq", color="col", zoom=zoom, width=width,
                                height=height)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_traces({'marker': {'size': markerSize}})
        fig.show()


if __name__ == "__main__":
    #_ap = str()
    _ap = visualizeFuzzyPatterns('soramame_frequentPatterns.txt', 10)
    _ap.visualize()