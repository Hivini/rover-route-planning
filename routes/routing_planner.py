import logging
import images.npy_image as npy_i
import routes.route_finder as rf

from typing import Tuple, Any, List
from simpleai.search import astar

MAP_FILE = 'data/map.npy'
MAP_SCALE = 10.0174
# The robot cannot move to another square based on this.
MAX_MOVE_HEIGHT = 0.25


class RoverManager(object):

    def __init__(self) -> None:
        self.map_image = npy_i.NpyImage(MAP_FILE, MAP_SCALE)

    def findRoute(self, sx: int, sy: int, ex: int, ey: int):
        """Finds a route from point A to point B on the map.

        Args:
            sx: Start X.
            sy: Start Y.
            ex: End X.
            ey: End Y.
        """
        logging.info('Finding route for x: %d y: %d to x: %d y: %d', sx, sy, ex, ey)
        # TODO: Validate points
        start_point = self._convertToRC(sx, sy)
        end_point = self._convertToRC(ex, ey)
        logging.info('Transformed route is x: %d y: %d to x: %d y: %d', start_point[0], start_point[1], end_point[0], end_point[1])
        result = astar(rf.RouteFinder(self.map_image.data, self.map_image.rows_n, self.map_image.columns_n,
                       start_point, end_point, MAX_MOVE_HEIGHT, invalid_height=-1), graph_search=True)
        return self._processResult(result)

    def _convertToRC(self, x: int, y: int) -> Tuple[int, int]:
        """Convers the coordinates x, y of the map into the row and column in the np.array

        Returns:
            A pair representing (row, column).
        """
        row = self.map_image.rows_n - round(y / MAP_SCALE)
        column = round(x / MAP_SCALE)
        return row, column

    def _processResult(self, result: Any) -> List[Tuple[int, int]]:
        points = []
        for _, (_, point) in enumerate(result.path()):
            points.append(point)
        return points