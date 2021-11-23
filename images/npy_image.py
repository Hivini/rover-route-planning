# npy_handler.py
import logging
from routes.region_classifier import RegionClassifier

import routes.routing_planner as rp
import matplotlib.lines as mlines
import numpy as np

from routes.utils import convertToImagePoint
from matplotlib import colors
from matplotlib import pyplot as plt
from matplotlib import patches as patches
from typing import Tuple, List


class NpyImageError(Exception):
    pass


class NpyImage(object):

    def __init__(self, file: str, scale: int) -> None:
        try:
            logging.info('Loading image in: %s', file)
            self.data = np.load(file)
        except IOError as e:
            logging.exception(e)
            raise NpyImageError('The image to load does not exists.')
        except ValueError as e:
            logging.exception(e)
            raise NpyImageError('There was an error while loading the image.')
        self.rows_n = len(self.data)
        if not self.rows_n > 0:
            raise NpyImageError('Cannot process empty images.')
        self.columns_n = len(self.data[0])
        self.scale = scale
        logging.info('Image -> rows:%d, columns:%d, scale:%.4f',
                     self.rows_n, self.columns_n, self.scale)
        self.regionClassifier = RegionClassifier(self.data, self.rows_n, self.columns_n)

    def setBaseImage(self, window_title: str, figure_title: str):
        """Setup the image visualization using Matplotlib."""
        cmap = plt.cm.get_cmap('autumn').copy()
        cmap.set_under(color='gray')
        ls = colors.LightSource(315, 45)
        rgb = ls.shade(self.data, cmap=cmap, vmin=0,
                       vmax=self.data.max(), vert_exag=2, blend_mode='hsv')
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title(window_title)

        ax.set_title(figure_title)
        image = ax.imshow(rgb, cmap=cmap, vmin=0, vmax=self.data.max(),
                          extent=[
                              0, self.scale * len(self.data[0]), 0, self.scale * len(self.data)],
                          interpolation='nearest', origin='upper')
        return fig, image, ax

    def showImage(self, window_title: str, figure_title: str) -> None:
        """Displays the NPY image using Matplot.

        This implementation is based from the professor's one but to a new version
        of matplotlib, to make it look similar.
        """
        fig, image, ax = self.setBaseImage(window_title, figure_title)
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')

    def showImagePoints(self, window_title: str, figure_title: str, start_point: Tuple[int, int], end_point: Tuple[int, int]) -> None:
        """Displays the NPY image using Matplot.

        This implementation is based from the professor's one but to a new version
        of matplotlib, to make it look similar.
        """
        fig, image, ax = self.setBaseImage(window_title, figure_title)
        plt.plot([start_point[0]], [start_point[1]],
                 marker='o', markersize=5, color="blue")
        plt.plot([end_point[0]], [end_point[1]],
                 marker='x', markersize=5, color="green")
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')

    def showImageWithPath(self, window_title: str, figure_title: str, paths: List[List[Tuple[int, int]]], points: List[Tuple[int, int]], names: List[str]) -> None:
        """Same us showImage but with the path as a line."""
        fig, image, ax = self.setBaseImage(window_title, figure_title)
        for path in paths:
            newPath = []
            for x, y in path:
                newPath.append(convertToImagePoint(x, y, self, rp.MAP_SCALE))
            x, y = zip(*newPath)
            line = mlines.Line2D(x, y, lw=2)
            ax.add_line(line)
            for i in range(len(points)):
                plt.plot([points[i][0]], [points[i][1]],
                         marker='o', markersize=3, color="black")
                ax.text(points[i][0] + 50, points[i][1], names[i])
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')

    def showImageWithSinglePath(self, window_title: str, figure_title: str, path: List[Tuple[int, int]], points: List[Tuple[int, int]], names: List[str], start_point: Tuple[int, int], end_point: Tuple[int, int]) -> None:
        """Same us showImage but with the path as a line."""
        fig, image, ax = self.setBaseImage(window_title, figure_title)
        newPath = []
        for x, y in path:
            newPath.append(convertToImagePoint(x, y, self, rp.MAP_SCALE))
        x, y = zip(*newPath)
        line = mlines.Line2D(x, y, lw=2)
        ax.add_line(line)
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')
        for i in range(len(points)):
            plt.plot([points[i][0]], [points[i][1]],
                     marker='o', markersize=2, color="black")
            ax.text(points[i][0], points[i][1], names[i])
        plt.plot([start_point[0]], [start_point[1]],
                 marker='o', markersize=8, color="green")
        plt.plot([end_point[0]], [end_point[1]],
                 marker='o', markersize=8, color="red")

    def showImagePointsMultiple(self, window_title: str, figure_title: str, points: List[Tuple[int, int]], names: List[str]) -> None:
        """Displays the NPY image using Matplot.

        This implementation is based from the professor's one but to a new version
        of matplotlib, to make it look similar.
        """
        fig, image, ax = self.setBaseImage(window_title, figure_title)
        for i in range(len(points)):
            plt.plot([points[i][0]], [points[i][1]],
                     marker='o', markersize=5, color="black")
            ax.text(points[i][0] + 20, points[i][1], names[i])
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')

    def showImageWithLines(self, window_title: str, figure_title: str, connections: List[Tuple[Tuple[int, int], Tuple[int, int]]], scale) -> None:
        """Same us showImage but with the path as a line."""
        fig, image, ax = self.setBaseImage(window_title, figure_title)
        for c in connections:
            x, y = zip(*c)
            line = mlines.Line2D(x, y, lw=2)
            ax.add_line(line)
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')

    def showImageRegions(self, window_title: str, figure_title: str):
        fig, image, ax = self.setBaseImage(window_title, figure_title)
        print(len(self.regionClassifier.regions))
        for i in range(len(self.regionClassifier.regions)):
            if i % 1000 == 0:
                print(i)
            bottomLeft = self.regionClassifier.regions[i].bottomLeft
            color = "green"
            if not self.regionClassifier.regions[i].isNav:
                color = "red"
            # Add plus one to avoid going off limits.
            x, y = convertToImagePoint(bottomLeft[1], bottomLeft[0], self, rp.MAP_SCALE)
            ax.add_patch(plt.Rectangle((x, y), 20 * rp.MAP_SCALE, 20 * rp.MAP_SCALE, color=color, alpha=0.5))
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')
