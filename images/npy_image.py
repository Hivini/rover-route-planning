# npy_handler.py
from matplotlib import colors
from matplotlib import pyplot as plt
import numpy as np


class NpyImage(object):

    def __init__(self, file: str, scale: int) -> None:
        self.image = np.load(file)
        self.scale = scale

    def showImage(self, window_title: str, figure_title: str) -> None:
        """Displays image using Matplot.

        This implementation is based from the professor's one but to a new version
        of matplotlib, to make it look similar.
        """
        cmap = plt.cm.get_cmap('autumn').copy()
        cmap.set_under(color='gray')
        ls = colors.LightSource(315, 45)
        rgb = ls.shade(self.image, cmap=cmap, vmin=0,
                       vmax=self.image.max(), vert_exag=2, blend_mode='hsv')
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title(window_title)

        ax.set_title(figure_title)
        image = ax.imshow(rgb, cmap=cmap, vmin=0, vmax=self.image.max(), extent=[
                          0, self.scale * len(self.image[0]), 0, self.scale * len(self.image)], interpolation='nearest', origin = 'upper')
        cbar = fig.colorbar(image, ax=ax)
        cbar.ax.set_ylabel('Height (m)')

        plt.show()
