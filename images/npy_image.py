# npy_handler.py
import logging
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
        plt.show()

    def showImageWithPath(self, window_title: str, figure_title: str, path: List[Tuple[int, int]], scale) -> None:
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
        plt.show()
