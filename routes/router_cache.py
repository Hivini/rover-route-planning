import logging
import os
import math
import numpy as np

from typing import Tuple, List

from numpy.lib import math
from routes.routing_planner import RoverManager
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
            nodeB.paths.append(self.existingPaths[i])
        return nodes

    def printGraph(self):
        for n in self.nodes:
            for child in n.next:
                print(n.name, '->', child)

    def findPath(self, rm: RoverManager, start_point: Tuple[int, int], end_point: Tuple[int, int], search_algorithm: SearchAlgorithm = SearchAlgorithm.ASTAR):
        start_closest = self._findClosest(start_point)
        end_closest = self._findClosest(end_point)
        start_path = rm.findRoute(
            start_point[0], start_point[1], start_closest.point[0], start_closest.point[1])
        if not start_path:
            raise Exception('No path found for start point to closest node')
        end_path = rm.findRoute(
            end_point[0], end_point[1], end_closest.point[0], end_closest.point[1])
        if not end_path:
            raise Exception('No path found for end point to closest node')
        graph_nodes = self._findGraphPath(start_closest, end_closest)

        graph_path = []
        past = graph_nodes[0]
        for i in range(1, len(graph_nodes)):
            index = -1
            for idx, val in enumerate(past.next):
                if val == graph_nodes[idx].name:
                    print()
                    index = idx
                    break
            graph_path.extend(past.paths[index])
            past = graph_nodes[i]
        fullPath = []
        fullPath.extend(start_path)
        fullPath.extend(graph_path)
        end_path.reverse()
        fullPath.extend(end_path)
        return fullPath

    def _findGraphPath(self, start: Node, end: Node):
        history = [start]
        aa = self._findHelper(start, end, history)
        if not aa:
            raise Exception('F')
        print('HIIIISTORY')
        for h in aa:
            print(h.name)
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

    def _findClosest(self, point: Tuple[int, int]) -> Node:
        node = self.nodes[0]
        closestDistance = self._findDistance(self.nodes[0].point, point)
        for i in range(1, len(self.nodes)):
            currentDistance = self._findDistance(self.nodes[i].point, point)
            if currentDistance < closestDistance:
                closestDistance = currentDistance
                node = self.nodes[i]
        return node

    def _findDistance(self, pointA: Tuple[int, int], pointB: Tuple[int, int]) -> float:
        return math.sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)
