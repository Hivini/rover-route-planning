import numpy as np
from typing import Tuple


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
