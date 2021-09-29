# main2.py
import routes.routing_planner as rp
import numpy as np
from routes.utils import SearchAlgorithm
from matplotlib import pyplot as plt
import os
import logging


POINTS = {
    "A": (1350, 16500),
    "B": (2800, 16500),
    "C": (4400, 16500),
    "D": (2710, 15430),
    "E": (1800, 13300),
    "F": (3500, 13600),
    "G": (5100, 13900),
    "H": (1800, 11800),
    "I": (3300, 11800),
    "J": (5400, 12060),
    "K": (1900, 10700),
    "L": (2100, 9700),
    "M": (4200, 9900),
    "N": (2280, 8910),
    "O": (2680, 7930),
    "P": (4450, 8000),
    "Q": (3500, 6210),
    "R": (6000, 6250),
    "S": (3170, 4820),
    "T": (4300, 5180),
    "U": (4780, 3650),
    "V": (4700, 2570),
    "W": (4500, 1630)
}

CONNECTIONS = [
    ("A", "B"),
    ("A", "D"),
    ("B", "C"),
    ("B", "D"),
    ("C", "D"),
    ("C", "G"),
    ("D", "E"),
    ("D", "F"),
    ("E", "F"),
    ("E", "H"),
    ("G", "J"),
    ("F", "G"),
    ("F", "I"),
    ("H", "I"),
    ("H", "K"),
    ("I", "J"),
    ("I", "M"),
    ("K", "L"),
    ("L", "N"),
    ("M", "O"),
    ("N", "O"),
    ("O", "P"),
    ("O", "Q"),
    ("P", "Q"),
    ("P", "R"),
    ("Q", "S"),
    ("Q", "T"),
    ("S", "T"),
    ("T", "U"),
    ("U", "V"),
    ("V", "W")
]

FILE = 'roads.npy'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

manager = rp.RoverManager()

manager.map_image.showImagePointsMultiple(
    'Rouver Points', 'Mars Map Overview', list(POINTS.values()))


roads = []

if os.path.exists(FILE):
    roads = np.load(FILE)
    print(roads)


else:
    aux = []
    for road in CONNECTIONS:
        aux.append([POINTS[road[0]], POINTS[road[1]]])
        print(road)
        path = manager.findRoute(
            POINTS[road[0]][0], POINTS[road[0]][1], POINTS[road[1]][0], POINTS[road[1]][1])
        if not path:
            logging.info(f"No solution was found for x: %d y: %d to x: %d y: %d",
                         POINTS[road[0]][0], POINTS[road[0]][1], POINTS[road[1]][0], POINTS[road[1]][1])
        roads.append(path)
    print("Caminos \n", roads)
    np.save(FILE, np.array(roads))
    #manager.map_image.showImageWithLines('Rouver Lines', 'Mars Map Overview', aux, rp.MAP_SCALE)

fullPath = []
for road in roads:
    print(road)
    break
    fullPath.extend(road)

# manager.map_image.showImageWithPath('Rover Route Planning', 'Mars Map Overview', fullPath, rp.MAP_SCALE)

# plt.show()
