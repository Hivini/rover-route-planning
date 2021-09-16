# npy_handler.py
import logging
import numpy as np

from matplotlib import colors
from matplotlib import pyplot as plt
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

    def showImage(self, window_title: str, figure_title: str) -> None:
        """Displays the NPY image using Matplot.

        This implementation is based from the professor's one but to a new version
        of matplotlib, to make it look similar.
        """
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
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')

        plt.show()
    
    def showImageWithPath(self, window_title: str, figure_title: str, path: List[Tuple[int, int]]) -> None:
        """Same us showImage but with the path."""
        # TODO(hivini): Improve, this is just a dirty hack.
        newData = self.data.copy()
        for _, (r, c) in enumerate(path):
            newData[r][c] = -1 

        cmap = plt.cm.get_cmap('autumn').copy()
        cmap.set_under(color='black')
        ls = colors.LightSource(315, 45)
        rgb = ls.shade(newData, cmap=cmap, vmin=0,
                       vmax=self.data.max(), vert_exag=2, blend_mode='hsv')
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title(window_title)

        ax.set_title(figure_title)
        image = ax.imshow(rgb, cmap=cmap, vmin=0, vmax=self.data.max(),
                          extent=[
                              0, self.scale * len(self.data[0]), 0, self.scale * len(self.data)],
                          interpolation='nearest', origin='upper')
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')

        plt.show()
