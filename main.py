# main.py
import logging
from routes.router_cache import RouteCache
import routes.routing_planner as rp
import time
from routes.utils import SearchAlgorithm
from matplotlib import pyplot as plt

START_X = 4325
START_Y = 4643
END_X = 5020
END_Y = 11983

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
manager = rp.RoverManager()
m = RouteCache(manager)
path = m.findPath(manager, (START_X, START_Y), (END_X, END_Y))
if path:
    manager.map_image.showImageWithSinglePath(
        'Rover Route Planning', 'Mars Map Overview', path)
plt.show()
