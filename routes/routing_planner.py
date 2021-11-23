import logging
import images.npy_image as npy_i
import routes.route_finder as rf

from routes.utils import SearchAlgorithm, convertToRC
from typing import Tuple, Any, List
from simpleai.search import astar, breadth_first, depth_first, greedy

MAP_FILE = 'data/map.npy'
MAP_SCALE = 10.0174
# The robot cannot move to another square based on this.
MAX_MOVE_HEIGHT = 0.25


class RoverManager(object):

    def __init__(self) -> None:
        self.map_image = npy_i.NpyImage(MAP_FILE, MAP_SCALE)

    def findRoute(self, sx: int, sy: int, ex: int, ey: int, search_algorithm: SearchAlgorithm = SearchAlgorithm.ASTAR):
        """Finds a route from point A to point B on the map.

        Args:
            sx: Start X.
            sy: Start Y.
            ex: End X.
            ey: End Y.
        """
        logging.info(
            'Finding route for x: %d y: %d to x: %d y: %d', sx, sy, ex, ey)
        start_point = convertToRC(sx, sy, self.map_image, MAP_SCALE)
        end_point = convertToRC(ex, ey, self.map_image, MAP_SCALE)
        logging.info('Transformed route is x: %d y: %d to x: %d y: %d',
                     start_point[0], start_point[1], end_point[0], end_point[1])
        route_finder = rf.RouteFinder(self.map_image.data, self.map_image.rows_n,
                                      self.map_image.columns_n, start_point, end_point, MAX_MOVE_HEIGHT, invalid_height=-1)
        if search_algorithm == SearchAlgorithm.ASTAR:
            logging.info('Using A* algorithm.')
            result = astar(route_finder, graph_search=True)
        elif search_algorithm == SearchAlgorithm.BREADTH_FIRST:
            logging.info('Using Breadth First algorithm.')
            result = breadth_first(route_finder, graph_search=True)
        elif search_algorithm == SearchAlgorithm.DEPTH_FIRST:
            logging.info('Using Depth First algorithm.')
            result = depth_first(route_finder, graph_search=True)
        else:
            logging.info('Using Greedy Best First algorithm.')
            result = greedy(route_finder, graph_search=True)
        if result:
            return self._processResult(result)
        return result

    def _processResult(self, result: Any) -> List[Tuple[int, int]]:
        points = []
        for _, (_, point) in enumerate(result.path()):
            points.append(point)
        return points
