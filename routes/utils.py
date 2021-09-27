import numpy as np

from typing import Tuple
from enum import Enum


class SearchAlgorithm(Enum):
    ASTAR = 0
    BREADTH_FIRST = 1
    DEPTH_FIRST = 2
    GREEDY_BEST_FIRST = 3


def convertToRC(x: int, y: int, map_image: np.array, scale: float) -> Tuple[int, int]:
    """Convers the coordinates x, y of the map into the row and column in the np.array

    Returns:
        A pair representing (row, column).
    """
    row = map_image.rows_n - round(y / scale)
    column = round(x / scale)
    return row, column


def convertToImagePoint(row: int, col: int, map_image: np.array, scale: float) -> Tuple[int, int]:
    """Convers the coordinates row, col of the array into the x and y in the image.

    Returns:
        A pair representing (x, y).
    """
    y = (map_image.rows_n - row) * scale
    x = col * scale
    return x, y
