# PlotLineGraphs4DataFrame is used to convert the given dataframe into a Line Graph.
#
#  **Importing this algorithm into a python program**
#
#     from PAMI.extras.graph import PlotLineGraphs4DataFrame as plt
#
#     dataFrame = pd.DataFrame(data)
#
#     obj = plt.PlotLineGraphs4DataFrame(dataFrame)
#
#     obj.plot(result=dataFrame, xaxis='minSup', yaxis='patterns', label='algorithm')
#
#     obj.plot(result=dataFrame, xaxis='minSup', yaxis='runtime', label='algorithm')
#
#     obj.plot(result=dataFrame, xaxis='minSup', yaxis='memoryRSS', label='algorithm')
#
#     obj.plot(result=dataFrame, xaxis='minSup', yaxis='memoryUSS', label='algorithm')
#
#     obj.save(result=dataFrame, xaxis='minSup', yaxis='patterns', label='algorithm', oFile='patterns.png')
#
#     obj.save(result=dataFrame, xaxis='minSup', yaxis='runtime', label='algorithm', oFile='runtime.png')
#
#     obj.save(result=dataFrame, xaxis='minSup', yaxis='memoryRSS', label='algorithm', oFile='memoryRSS.png')
#
#     obj.save(result=dataFrame, xaxis='minSup', yaxis='memoryUSS', label='algorithm', oFile='memoryUSS.png')
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

import matplotlib.pyplot as plt
import pandas as pd


class PlotLineGraphs4DataFrame:
    """
    A class to generate and save line graphs from a given DataFrame.

    :Attributes:
        dataFrame (pd.DataFrame): Input DataFrame to generate graphs.

    :Methods:
        plot(result, xaxis, yaxis, label): Plots a line graph based on the specified axes.
        save(result, xaxis, yaxis, label, oFile): Saves the line graph to the specified file.
    """

    def __init__(self, dataFrame: pd.DataFrame) -> None:
        """
        Initialize the class with a DataFrame.

        :param dataFrame: Input DataFrame
        """
        self.dataFrame = dataFrame

    def plot(self, result: pd.DataFrame, xaxis: str, yaxis: str, label: str) -> None:
        """
        Plots a line graph.

        :param result: Input DataFrame
        :param xaxis: Column name for the x-axis
        :param yaxis: Column name for the y-axis
        :param label: Column name to use for legend labels
        """
        plt.figure()
        for key, grp in result.groupby(label):
            plt.plot(grp[xaxis], grp[yaxis], label=f"{label}: {key}")
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)
        plt.title(f"{yaxis} vs {xaxis}")
        plt.legend()
        plt.show()
        print(f"Graph for {yaxis} vs {xaxis} is successfully generated!")

    def save(self, result: pd.DataFrame, xaxis: str, yaxis: str, label: str, oFile: str) -> None:
        """
        Saves the line graph to a file.

        :param result: Input DataFrame
        :param xaxis: Column name for the x-axis
        :param yaxis: Column name for the y-axis
        :param label: Column name to use for legend labels
        :param oFile: Output file name to save the graph
        """
        plt.figure()
        for key, grp in result.groupby(label):
            plt.plot(grp[xaxis], grp[yaxis], label=f"{label}: {key}")
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)
        plt.title(f"{yaxis} vs {xaxis}")
        plt.legend()
        plt.savefig(oFile)
        plt.close()
        print(f"Graph saved as {oFile}!")

if __name__ == "__main__":
    # Example DataFrame
    data = {
        'algorithm': ['FPGrowth', 'FPGrowth', 'FPGrowth', 'FPGrowth', 'FPGrowth'],
        'minSup': [0.01, 0.02, 0.03, 0.01, 0.02],
        'patterns': [386, 155, 60, 386, 155],
        'runtime': [7.35, 4.66, 4.66, 4.57, 2.51],
        'memoryRSS': [426545152, 309182464, 241397760, 233537536, 267165696],
        'memoryUSS': [426545152, 309182464, 241397760, 233537536, 267165696]
    }
    dataFrame_ = pd.DataFrame(data)

    obj = PlotLineGraphs4DataFrame(dataFrame_)

    obj.plot(result=dataFrame_, xaxis='minSup', yaxis='patterns', label='algorithm')
    obj.plot(result=dataFrame_, xaxis='minSup', yaxis='runtime', label='algorithm')
    obj.plot(result=dataFrame_, xaxis='minSup', yaxis='memoryRSS', label='algorithm')
    obj.plot(result=dataFrame_, xaxis='minSup', yaxis='memoryUSS', label='algorithm')

    obj.save(result=dataFrame_, xaxis='minSup', yaxis='patterns', label='algorithm', oFile='patterns.png')
    obj.save(result=dataFrame_, xaxis='minSup', yaxis='runtime', label='algorithm', oFile='runtime.png')
    obj.save(result=dataFrame_, xaxis='minSup', yaxis='memoryRSS', label='algorithm', oFile='memoryRSS.png')
    obj.save(result=dataFrame_, xaxis='minSup', yaxis='memoryUSS', label='algorithm', oFile='memoryUSS.png')
