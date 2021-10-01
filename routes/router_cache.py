import logging
import os
import math
import numpy as np

from typing import Tuple, List

from numpy.lib import math
from routes.routing_planner import MAP_SCALE, RoverManager
from routes.utils import SearchAlgorithm

POINTS = {
    'A': (4697, 2891),
    'B': (4650, 3996),
    'C': (4210, 5233),
    'D': (3676, 6010),
    'E': (3283, 6900),
    'F': (2813, 7695),
    'G': (2514, 8233),
    'H': (2136, 9378),
    'I': (2006, 9946),
    'J': (1758, 10667),
    'K': (3331, 8095),
    'L': (3919, 8398),
    'M': (4841, 7770),
    'N': (5368, 7019),
    'O': (3876, 9885),
    'P': (3536, 10971),
    'Q': (4574, 11885),
    'R': (5838, 12724),
    'S': (5678, 14111),
    'T': (1433, 12847)
}

CONNECTIONS = [
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'),
    ('E', 'F'),
    ('F', 'G'),
    ('G', 'H'),
    ('H', 'I'),
    ('I', 'J'),
    ('F', 'K'),
    ('K', 'L'),
    ('L', 'M'),
    ('M', 'N'),
    ('L', 'O'),
    ('O', 'P'),
    ('P', 'Q'),
    ('Q', 'R'),
    ('R', 'S'),
    ('S', 'T')
]

FILE = 'roads.npy'


class Node(object):
    def __init__(self) -> None:
        self.name = None
        self.point = None
        self.next = []
        self.paths = []


class RouteCache:

    def __init__(self, rm: RoverManager):
        if os.path.exists(FILE):
            self.existingPaths = np.load(FILE, allow_pickle=True)
        else:
            paths = self._createPaths(rm)
            np.save(FILE, np.array(paths, dtype=object))
            self.existingPaths = paths
        rm.map_image.showImageWithPath('Rover Route Planning', 'Mars Map Overview', self.existingPaths, list(
            POINTS.values()), list(POINTS.keys()))
        self.nodes = self._buildGraph()

    def _createPaths(self, rm: RoverManager):
        paths = []
        for a, b in CONNECTIONS:
            start = POINTS[a]
            end = POINTS[b]
            route = rm.findRoute(start[0], start[1], end[0], end[1])
            if not route:
                logging.info('Aiudaaaaa')
            paths.append(route)
        return paths

    def _buildGraph(self) -> List[Node]:
        nodes: List[Node] = []
        for i in range(len(CONNECTIONS)):
            a = CONNECTIONS[i][0]
            b = CONNECTIONS[i][1]
            found = False
            nodeA = None
            nodeB = None
            for n in nodes:
                if n.name == a:
                    nodeA = n
                if n.name == b:
                    nodeB = n
                if n.name == a and b in n.next:
                    found = True
                    break
            if found:
                continue
            if not nodeA:
                nodeA = Node()
                nodeA.name = a
                nodeA.point = POINTS[a]
                nodes.append(nodeA)
            nodeA.next.append(b)
            nodeA.paths.append(self.existingPaths[i])

            if not nodeB:
                nodeB = Node()
                nodeB.name = b
                nodeB.point = POINTS[b]
                nodes.append(nodeB)
            nodeB.next.append(a)
            invertedCoolKid = self.existingPaths[i].copy()
            invertedCoolKid.reverse()
            nodeB.paths.append(invertedCoolKid)
        return nodes

    def printGraph(self):
        for n in self.nodes:
            for child in n.next:
                print(n.name, '->', child)

    def findPath(self, rm: RoverManager, start_point: Tuple[int, int], end_point: Tuple[int, int], search_algorithm: SearchAlgorithm = SearchAlgorithm.ASTAR):
        """Finds a path using the graph."""
        start_closests = self._findClosestList(start_point)
        end_closests = self._findClosestList(end_point)
        if (self._findDistance(start_closests[0].point, start_point) > self._findDistance(end_point, start_point) and self._findDistance(end_closests[0].point, end_point) > self._findDistance(end_point, start_point)):
            path = rm.findRoute(
                start_point[0], start_point[1], end_point[0], end_point[1], search_algorithm)
            rm.map_image.showImageWithSinglePath('Rover Route Planning', 'Mars Map Overview', path, list(
                POINTS.values()), list(POINTS.keys()), start_point, end_point)
            return path
        start_node_paths = self._findPathOfListNodes(
            rm, start_point, start_closests, search_algorithm)
        end_node_paths = self._findPathOfListNodes(
            rm, end_point, end_closests, search_algorithm)
        if not start_node_paths or not end_node_paths:
            path = rm.findRoute(
                start_point[0], start_point[1], end_point[0], end_point[1], search_algorithm)
            if not path:
                raise Exception('No possible path could be found.')
        start_path, start_closest = start_node_paths
        end_path, end_closest = end_node_paths
        if self._findDistance(start_point, end_point) < self._findDistance(start_point, start_closest.point) + self._findDistance(end_point, end_closest.point):
            path = rm.findRoute(
                start_point[0], start_point[1], end_point[0], end_point[1], search_algorithm)
            rm.map_image.showImageWithSinglePath('Rover Route Planning', 'Mars Map Overview', path, list(
                POINTS.values()), list(POINTS.keys()), start_point, end_point)
            return path
        graph_nodes = self._findGraphPath(start_closest, end_closest)
        graph_path = []
        past = graph_nodes[0]
        for i in range(1, len(graph_nodes)):
            index = -1
            for idx, val in enumerate(past.next):
                if val == graph_nodes[i].name:
                    index = idx
                    break
            graph_path.extend(past.paths[index])
            past = graph_nodes[i]
        fullPath = []
        fullPath.extend(start_path)
        fullPath.extend(graph_path)
        end_path.reverse()
        fullPath.extend(end_path)
        rm.map_image.showImageWithSinglePath('Rover Route Planning', 'Mars Map Overview', fullPath, list(
            POINTS.values()), list(POINTS.keys()), start_point, end_point)
        return fullPath

    def _findPathOfListNodes(self, rm: RoverManager, point: Tuple[int, int], closests: List[Node], search_algorithm: SearchAlgorithm):
        """Returns the closest possible node of the graph."""
        for n in closests:
            path = rm.findRoute(
                point[0], point[1], n.point[0], n.point[1], search_algorithm=search_algorithm)
            if path:
                return path, n
        return None

    def _findGraphPath(self, start: Node, end: Node):
        """Depth First search algorithm to connect two points in the graph."""
        history = [start]
        aa = self._findHelper(start, end, history)
        if not aa:
            raise Exception('F')
        return aa

    def _findHelper(self, current: Node, end: Node, history: List[Node]):
        if (current == end):
            return history
        for n in current.next:
            for existing in self.nodes:
                if existing.name == n:
                    realNode = existing
                    break
            if realNode not in history:
                newHistory = history.copy()
                newHistory.append(realNode)
                result = self._findHelper(realNode, end, newHistory)
                if result:
                    return result
        return None

    def _findClosestList(self, point: Tuple[int, int]) -> Node:
        """Returns a list with the all the nodes ordered by distance of the point."""
        nodes = [self.nodes[0]]
        distances = [self._findDistance(self.nodes[0].point, point)]
        for i in range(1, len(self.nodes)):
            newDistance = self._findDistance(self.nodes[i].point, point)
            for y in range(len(distances)):
                if newDistance < distances[y]:
                    distances.insert(y, newDistance)
                    nodes.insert(y, self.nodes[i])
                    break
                else:
                    if y == len(distances) - 1:
                        distances.append(newDistance)
                        nodes.append(self.nodes[i])
                        break
        return nodes

    def _findDistance(self, pointA: Tuple[int, int], pointB: Tuple[int, int]) -> float:
        return math.sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)
